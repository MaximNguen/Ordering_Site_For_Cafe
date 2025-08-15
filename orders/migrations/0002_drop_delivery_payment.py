from django.db import migrations


class Migration(migrations.Migration):

	dependencies = [
		('orders', '0001_initial'),
	]

	operations = [
		migrations.RunSQL(
			sql=(
				"""
				ALTER TABLE orders_order DROP COLUMN IF EXISTS delivery_method;
				ALTER TABLE orders_order DROP COLUMN IF EXISTS payment_method;
				"""
			),
			reverse_sql=(
				"""
				ALTER TABLE orders_order ADD COLUMN IF NOT EXISTS delivery_method varchar(50) NULL;
				ALTER TABLE orders_order ADD COLUMN IF NOT EXISTS payment_method varchar(50) NULL;
				"""
			),
		),
	]


