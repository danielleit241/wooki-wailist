"""allow duplicate referral code

Revision ID: 9b2d1f7c4a10
Revises: 4ae819736523
Create Date: 2026-02-23 22:40:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9b2d1f7c4a10"
down_revision: Union[str, Sequence[str], None] = "4ae819736523"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index(op.f("ix_waiting_list_users_referral_code"), table_name="waiting_list_users")
    op.create_index(
        op.f("ix_waiting_list_users_referral_code"),
        "waiting_list_users",
        ["referral_code"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_waiting_list_users_referral_code"), table_name="waiting_list_users")
    op.create_index(
        op.f("ix_waiting_list_users_referral_code"),
        "waiting_list_users",
        ["referral_code"],
        unique=True,
    )
