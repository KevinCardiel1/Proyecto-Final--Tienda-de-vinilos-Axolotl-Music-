from django import forms
from .models import Artista, Producto, Usuario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms as django_forms


class ArtistaForm(forms.ModelForm):
    class Meta:
        model = Artista
        fields = ['nombre_artista', 'descripcion', 'foto']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows':4}),
        }


class ProductoForm(forms.ModelForm):
    # Definir las opciones permitidas en el formulario (solo las 4 del navbar)
    NAVBAR_GENEROS = [
        ('', '---------'),
        ('pop', 'Pop'),
        ('k-pop', 'K-Pop'),
        ('rock', 'Rock'),
        ('latino', 'Latino'),
    ]

    # Mantener required=True para validación; la opción vacía aparece como placeholder.
    genero = forms.ChoiceField(choices=NAVBAR_GENEROS, required=True)

    class Meta:
        model = Producto
        fields = ['artista', 'nombre_producto', 'genero', 'tipo', 'descripcion', 'stock', 'precio', 'novedad', 'img']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows':3}),
            'tipo': forms.Select(choices=Producto.TIPO_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        # Si se edita un producto que ya tiene un género fuera de las 4 permitidas,
        # incluir ese valor en las opciones para no invalidar ni perder datos existentes.
        super().__init__(*args, **kwargs)
        allowed_values = [v for v, _ in self.NAVBAR_GENEROS]
        instance = kwargs.get('instance') if 'instance' in kwargs else getattr(self, 'instance', None)
        # Fallback: also check self.instance if present
        current = None
        try:
            current = instance.genero if instance else (self.instance.genero if hasattr(self, 'instance') else None)
        except Exception:
            current = None

        if current and current not in allowed_values:
            # obtener etiqueta desde los choices del modelo si existe
            label = dict(Producto.GENEROS_CHOICES).get(current, str(current).capitalize())
            # insertar la opción actual al final, preservando la opción vacía inicial
            self.fields['genero'].choices = self.NAVBAR_GENEROS + [(current, label)]
        else:
            self.fields['genero'].choices = self.NAVBAR_GENEROS


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'tel', 'direccion', 'codigo_postal', 'profile_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # labels in Spanish
        self.fields['nombre'].label = 'Nombre'
        self.fields['email'].label = 'Email'
        self.fields['tel'].label = 'Teléfono'
        self.fields['direccion'].label = 'Dirección'
        self.fields['codigo_postal'].label = 'Código postal'
        self.fields['profile_image'].label = 'Foto de perfil'


class EmpleadoCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Etiquetas en español
        self.fields['username'].label = 'Nombre de usuario'
        # Reemplazar el help_text por defecto (inglés) por uno en español
        self.fields['username'].help_text = 'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ únicamente.'

        self.fields['password1'].label = 'Contraseña'
        self.fields['password1'].help_text = 'Tu contraseña debe contener al menos 8 caracteres y no ser fácilmente adivinable.'

        self.fields['password2'].label = 'Confirmación de contraseña'
        self.fields['password2'].help_text = 'Introduce la misma contraseña de antes, para verificación.'

        # Campo teléfono (no parte del User, lo guardaremos en Usuario)
        self.fields['tel'] = forms.CharField(label='Teléfono', required=False)

    def clean_password2(self):
        # Usar la validación estándar pero asegurar mensajes en español cuando falte coincidencia
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise django_forms.ValidationError('Las contraseñas no coinciden.')
        return password2


class EmpleadoUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['username'].help_text = 'Requerido. 150 caracteres o menos.'
        self.fields['email'].label = 'Email'
        self.fields['email'].help_text = ''
        # Teléfono desde el perfil Usuario
        self.fields['tel'] = forms.CharField(label='Teléfono', required=False)
        # Si tenemos instancia con perfil, inicializar
        instance = kwargs.get('instance') if 'instance' in kwargs else None
        if instance and hasattr(instance, 'usuario'):
            try:
                self.fields['tel'].initial = instance.usuario.tel
            except Exception:
                self.fields['tel'].initial = ''
