from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    IntegerField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    InputRequired,
    NumberRange
)


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(
                message="El nombre del producto es obligatorio."
            ),
            Length(
                min=3,
                max=80,
                message="El nombre debe tener entre 3 y 80 caracteres."
            )
        ]
    )

    categoria = SelectField(
        "Categoría",
        choices=[
            ("", "Seleccione una categoría"),
            ("Fuerza", "Fuerza"),
            ("Movilidad", "Movilidad"),
            ("Accesorios", "Accesorios"),
            ("Ropa deportiva", "Ropa deportiva")
        ],
        validators=[
            DataRequired(
                message="Debe seleccionar una categoría."
            )
        ]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[
            DataRequired(
                message="La descripción del producto es obligatoria."
            ),
            Length(
                min=10,
                max=250,
                message="La descripción debe tener entre 10 y 250 caracteres."
            )
        ]
    )

    stock = IntegerField(
        "Stock",
        validators=[
            InputRequired(
                message="El stock es obligatorio."
            ),
            NumberRange(
                min=0,
                max=1000,
                message="El stock debe ser un número entre 0 y 1000."
            )
        ]
    )

    submit = SubmitField(
        "Guardar producto"
    )