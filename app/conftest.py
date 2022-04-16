import pytest
from mixer.backend.django import mixer
from app.users.models import User
from app.accounts.models import LoanAccount

default_amount = (100.00, "ZAR")


@pytest.fixture()
def admin_user(db):
    return User.objects.create_superuser(
        first_name="Admin",
        last_name="User",
        phone_number="+0987654321",
        password="adminuser",
    )


@pytest.fixture()
def auth_user(db):
    return User.objects.create_user(
        first_name="First",
        last_name="Last",
        phone_number="+1234567890",
        password="firstlast",
    )


@pytest.fixture()
def other_user(db):
    return User.objects.create_user(
        first_name="Other",
        last_name="User",
        phone_number="+1234567899",
        password="otheruser",
    )


@pytest.fixture()
def admin_account(db, admin_user):
    return mixer.blend(LoanAccount, user=admin_user, principal=default_amount)


@pytest.fixture()
def auth_account(db, auth_user):
    return mixer.blend(LoanAccount, user=auth_user, principal=default_amount)
