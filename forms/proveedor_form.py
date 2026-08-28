from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length
)


class ProveedorForm(FlaskForm):

    nombre = StringField(
        "Nombre del proveedor",
        validators=[
            DataRequired(
                message="El nombre del proveedor es obligatorio."
            ),
            Length(
                min=3,
                max=80,
                message="El nombre debe tener entre 3 y 80 caracteres."
            )
        ]
    )

    productos = StringField(
        "Productos suministrados",
        validators=[
            DataRequired(
                message="Debe indicar los productos suministrados."
            ),
            Length(
                min=3,
                max=150,
                message="La descripción de los productos debe tener entre 3 y 150 caracteres."
            )
        ]
    )

    contacto = StringField(
        "Contacto",
        validators=[
            DataRequired(
                message="El contacto del proveedor es obligatorio."
            ),
            Length(
                min=7,
                max=30,
                message="El contacto debe tener entre 7 y 30 caracteres."
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
        "Proveedor activo",
        default=True
    )

    submit = SubmitField(
        "Guardar proveedor"
    )