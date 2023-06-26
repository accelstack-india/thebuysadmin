from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class RegistrationModel:
    fname: str
    lname: str
    email: str
    phone: str
    age: str
    password: str

    @staticmethod
    def from_dict(obj: Any) -> 'RegistrationModel':
        assert isinstance(obj, dict)
        fname = from_str(obj.get("fname"))
        lname = from_str(obj.get("lname"))
        email = from_str(obj.get("email"))
        phone = from_str(obj.get("phone"))
        age = from_str(obj.get("age"))
        password = from_str(obj.get("password"))
        return RegistrationModel(fname, lname, email, phone, age, password)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fname"] = from_str(self.fname)
        result["lname"] = from_str(self.lname)
        result["email"] = from_str(self.email)
        result["phone"] = from_str((self.phone))
        result["age"] = from_str(self.age)
        result["password"] = from_str(self.password)
        return result


def registration_model_from_dict(s: Any) -> RegistrationModel:
    return RegistrationModel.from_dict(s)


def registration_model_to_dict(x: RegistrationModel) -> Any:
    return to_class(RegistrationModel, x)
