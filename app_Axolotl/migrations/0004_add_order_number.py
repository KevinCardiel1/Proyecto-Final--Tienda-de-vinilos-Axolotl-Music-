from django.db import migrations, models


def forwards(apps, schema_editor):
    Pedido = apps.get_model('app_Axolotl', 'Pedido')
    Usuario = apps.get_model('app_Axolotl', 'Usuario')

    # Para cada usuario, asignar números secuenciales a sus pedidos ordenados por fecha
    for usuario in Usuario.objects.all():
        pedidos = Pedido.objects.filter(usuario=usuario).order_by('fecha')
        num = 1
        for p in pedidos:
            p.order_number = num
            p.save(update_fields=['order_number'])
            num += 1


def reverse(apps, schema_editor):
    Pedido = apps.get_model('app_Axolotl', 'Pedido')
    # Dejar en NULL los order_number al revertir
    Pedido.objects.update(order_number=None)


class Migration(migrations.Migration):

    dependencies = [
        ('app_Axolotl', '0003_alter_producto_genero_alter_producto_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='order_number',
            field=models.PositiveIntegerField(blank=True, null=True, help_text='Número de pedido secuencial por usuario'),
        ),
        migrations.RunPython(forwards, reverse),
    ]
