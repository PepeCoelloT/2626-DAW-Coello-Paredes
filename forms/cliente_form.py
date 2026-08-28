from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email
)


class ClienteForm(FlaskForm):

    nombre = StringField(
        "Nombre completo",
        validators=[
            DataRequired(
                message="El nombre del cliente es obligatorio."
            ),
            Length(
                min=3,
                max=80,
                message="El nombre debe tener entre 3 y 80 caracteres."
            )
        ]
    )

    correo = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(
                message="El correo electrónico es obligatorio."
            ),
            Email(
                message="Ingrese un correo electrónico válido."
            ),
            Length(
                max=120,
                message="El correo no puede superar los 120 caracteres."
            )
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(
                message="El teléfono es obligatorio."
            ),
            Length(
                min=7,
                max=15,
                message="El teléfono debe tener entre 7 y 15 caracteres."
            )
        ]
    )

    ciudad = StringField(
        "Ciudad",
        validators=[
            DataRequired(
                message="La ciudad es obligatoria."
            ),
            Length(
                min=2,
                max=60,
                message="La ciudad debe tener entre 2 y 60 caracteres."
            )
        ]
    )

    activo = BooleanField(
        "Cliente activo",
        default=True
    )

    submit = SubmitField(
        "Guardar cliente"
    )