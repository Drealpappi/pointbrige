from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_email_alter_user_id_alter_user_is_admin_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE accounts_user
                ADD COLUMN IF NOT EXISTS referral_code varchar(20);

                ALTER TABLE accounts_user
                ADD COLUMN IF NOT EXISTS referred_by bigint;

                ALTER TABLE accounts_user
                ADD COLUMN IF NOT EXISTS is_client boolean NOT NULL DEFAULT true;

                ALTER TABLE accounts_user
                ADD COLUMN IF NOT EXISTS is_admin boolean NOT NULL DEFAULT false;

                ALTER TABLE accounts_user
                ADD COLUMN IF NOT EXISTS is_staff boolean NOT NULL DEFAULT false;

                CREATE UNIQUE INDEX IF NOT EXISTS accounts_user_referral_code_unique
                ON accounts_user (referral_code);

                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conname = 'accounts_user_referred_by_id_fk'
                    ) THEN
                        ALTER TABLE accounts_user
                        ADD CONSTRAINT accounts_user_referred_by_id_fk
                        FOREIGN KEY (referred_by)
                        REFERENCES accounts_user(id)
                        DEFERRABLE INITIALLY DEFERRED;
                    END IF;
                END
                $$;
            """,
            reverse_sql="""
                ALTER TABLE accounts_user
                DROP CONSTRAINT IF EXISTS accounts_user_referred_by_id_fk;

                DROP INDEX IF EXISTS accounts_user_referral_code_unique;

                ALTER TABLE accounts_user
                DROP COLUMN IF EXISTS referred_by;

                ALTER TABLE accounts_user
                DROP COLUMN IF EXISTS referral_code;

                ALTER TABLE accounts_user
                DROP COLUMN IF EXISTS is_client;

                ALTER TABLE accounts_user
                DROP COLUMN IF EXISTS is_admin;
            """,
        ),
    ]