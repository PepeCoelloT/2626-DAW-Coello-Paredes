from decimal import Decimal

from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    DateField,
    SelectField,
    BooleanField,
    IntegerField,
    DecimalField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length,
    InputRequired,
    NumberRange
)


class FacturacionForm(FlaskForm):

    numero = StringField(
        "Número de factura",
        validators=[
            DataRequired(
                message="El número de factura es obligatorio."
            ),
            Length(
                min=3,
                max=30,
                message="El número de factura debe tener entre 3 y 30 caracteres."
            )
        ]
    )

    fecha = DateField(
        "Fecha",
        format="%Y-%m-%d",
        validators=[
            DataRequired(
                message="La fecha es obligatoria."
            )
        ]
    )

    cliente_id = SelectField(
        "Cliente",
        choices=[],
        coerce=int,
        validators=[
            DataRequired(
                message="Debe seleccionar un cliente."
            )
        ]
    )

    forma_pago = SelectField(
        "Forma de pago",
        choices=[
            ("", "Seleccione una forma de pago"),
            ("Efectivo", "Efectivo"),
            ("Tarjeta", "Tarjeta"),
            ("Transferencia", "Transferencia")
        ],
        validators=[
            DataRequired(
                message="Debe seleccionar una forma de pago."
            )
        ]
    )

    pagada = BooleanField(
        "Factura pagada",
        default=True
    )

    producto_id = SelectField(
        "Producto",
        choices=[],
        coerce=int,
        validators=[
            DataRequired(
                message="Debe seleccionar un producto."
            )
        ]
    )

    cantidad = IntegerField(
        "Cantidad",
        validators=[
            InputRequired(
                message="La cantidad es obligatoria."
            ),
            NumberRange(
                min=1,
                max=100,
                message="La cantidad debe estar entre 1 y 100."
            )
        ]
    )

    precio = DecimalField(
        "Precio unitario",
        places=2,
        rounding=None,
        validators=[
            InputRequired(
                message="El precio unitario es obligatorio."
            ),
            NumberRange(
                min=Decimal("0.01"),
                max=Decimal("10000.00"),
                message="El precio debe ser mayor a 0 y no superar los $10.000."
            )
        ]
    )

    submit = SubmitField(
        "Guardar factura"
    )