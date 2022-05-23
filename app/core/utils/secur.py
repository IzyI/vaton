import base64
import re
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from zxcvbn import zxcvbn

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encode_vigenere(key: str, clear: str) -> str:
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


def decode_vigenere(key: str, enc: str) -> str:
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
    return pwd_context.verify(
        plain_password[:3]
        + salt[:5]
        + plain_password[:5]
        + salt[5:]
        + plain_password[2:],
        hashed_password,
    )


def get_password_hash(password: str, salt: str) -> str:
    return pwd_context.hash(
        password[:3] + salt[:5] + password[:5] + salt[5:] + password[2:]
    )


def decode_jwt(token: str, secret: str, algorithm: str):
    result = jwt.decode(token, secret, algorithms=[algorithm])
    return result


def check_time_jwt(time: int) -> bool:
    if datetime.utcnow().timestamp() < time:
        return True
    else:
        return False


def encode_jwt(data: dict, secret: str, algorithm: str, expire_minute=10) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=expire_minute)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=algorithm)
    return encoded_jwt


def clean_email(_email: str) -> str:
    local_part, global_part = _email.rsplit("@", 1)
    if "+" in local_part:
        _email = f"{local_part.split('+')[0]}@{global_part}"
    return _email


def is_valid_email(email: str) -> bool:
    regex = re.compile(
        r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"  # noqa
    )
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def is_valid_domain(domain: str) -> bool:
    regex = re.compile(
        r"^(((?!\-))(xn\-\-)?[a-z0-9\-_]{0,61}[a-z0-9]\.)*(xn\-\-)?([a-z0-9\-]{1,61}|[a-z0-9\-]{1,30})\.[a-z]{2,}$"  # noqa
    )
    if re.fullmatch(regex, domain):
        return True
    else:
        return False


def is_password_regex(password: str) -> tuple:
    regex_list_pass_check = (
        (
            r"[a-z]",
            "Weak password: password must contain one lowercase character at least.",
        ),
        (
            r"[A-Z]",
            "Weak password: password must contain one uppercase character at least.",
        ),
        (r"[0-9]", "Weak password: password must contain one number at least."),
        (
            r'[ >=<#$%&\\\'_"!()*+,-./:;=?@\[\]^_`{|}~\]\[]',
            "Weak password: password must contain one special character at least.",
        ),
        (r"^.{8,}", "Weak password: password must contain 8 characters at least."),
    )
    for r in regex_list_pass_check:
        if not re.search(r[0], str(password)):
            return False, r[1]
    if len(password) > 256:
        return False, "Weak password: password must be no more than 256 characters."
    return True, None


def is_password_weak(password: str, email: str = None, username: str = None):
    kwargs = {}
    if email:
        kwargs.update({"user_inputs": [email, username]})

    res = zxcvbn(password, **kwargs)
    if res["score"] > 2:
        return False

    return res["feedback"]
