from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo
)


class UsuarioForm(FlaskForm):

    usuario = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired(
                message="El nombre de usuario es obligatorio."
            ),
            Length(
                min=3,
                max=50,
                message="El usuario debe tener entre 3 y 50 caracteres."
            )
        ]
    )


    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(
                message="La contraseña es obligatoria."
            ),
            Length(
                min=6,
                max=128,
                message="La contraseña debe tener al menos 6 caracteres."
            )
        ]
    )


    confirmar_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(
                message="Debe confirmar la contraseña."
            ),
            EqualTo(
                "password",
                message="Las contraseñas no coinciden."
            )
        ]
    )


    submit = SubmitField(
        "Registrar usuario"
    )