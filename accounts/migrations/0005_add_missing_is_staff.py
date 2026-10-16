from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "accounts",
            "0004_repair_user_schema",
        ),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE accounts_user
                ADD COLUMN IF NOT EXISTS is_staff
                boolean NOT NULL DEFAULT false;
            """,
            reverse_sql="""
                ALTER TABLE accounts_user
                DROP COLUMN IF EXISTS is_staff;
            """,
        ),
    ]