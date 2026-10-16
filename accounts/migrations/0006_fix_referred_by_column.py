from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "accounts",
            "0005_add_missing_is_staff",
        ),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE accounts_user
                RENAME COLUMN referred_by TO referred_by_id;
            """,
            reverse_sql="""
                ALTER TABLE accounts_user
                RENAME COLUMN referred_by_id TO referred_by;
            """,
        ),
    ]