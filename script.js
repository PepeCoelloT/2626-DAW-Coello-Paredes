// ==============================================
// SCRIPT.JS - SEMANA 8
// FitZone Store
// Bootstrap, contenido dinámico, modal y spinner
// ==============================================

document.addEventListener("DOMContentLoaded", function () {

    // ==============================================
    // CAPTURA DE ELEMENTOS DEL HTML
    // ==============================================

    const formulario =
        document.getElementById("formularioRegistro");

    const nombreRegistro =
        document.getElementById("nombreRegistro");

    const descripcionRegistro =
        document.getElementById("descripcionRegistro");

    const categoriaRegistro =
        document.getElementById("categoriaRegistro");

    const contenedorProductos =
        document.getElementById("contenedorProductos");

    const totalRegistros =
        document.getElementById("totalRegistros");

    const mensajeValidacion =
        document.getElementById("mensajeValidacion");

    const spinnerCarga =
        document.getElementById("spinnerCarga");


    // ==============================================
    // ELEMENTOS DEL MODAL BOOTSTRAP
    // ==============================================

    const modalProducto =
        document.getElementById("modalProducto");

    const modalTitulo =
        document.getElementById("modalTitulo");

    const modalImagen =
        document.getElementById("modalImagen");

    const modalDescripcion =
        document.getElementById("modalDescripcion");

    const modalCategoria =
        document.getElementById("modalCategoria");

    const modalEstado =
        document.getElementById("modalEstado");


    // ==============================================
    // ARREGLO DE OBJETOS CON PRODUCTOS INICIALES
    // ==============================================

    let productos = [

        {
            id: 1,
            nombre: "Bandas elásticas",
            descripcion:
                "Ideales para ejercicios de fuerza, movilidad, calentamiento y entrenamiento funcional.",
            categoria: "Fuerza",
            disponible: true,
            imagen: "imagenes/Bandas elásticas.png"
        },

        {
            id: 2,
            nombre: "Mancuernas",
            descripcion:
                "Accesorios prácticos para entrenar brazos, hombros, espalda y piernas.",
            categoria: "Fuerza",
            disponible: true,
            imagen: "imagenes/mancuernas.png"
        },

        {
            id: 3,
            nombre: "Colchonetas",
            descripcion:
                "Recomendadas para yoga, abdominales, estiramientos y ejercicios de bajo impacto.",
            categoria: "Movilidad",
            disponible: false,
            imagen: "imagenes/Colchonetas.png"
        },

        {
            id: 4,
            nombre: "Botellas deportivas",
            descripcion:
                "Útiles para mantener una correcta hidratación durante cualquier actividad física.",
            categoria: "Accesorios",
            disponible: true,
            imagen: "imagenes/Botellas deportivas.png"
        },

        {
            id: 5,
            nombre: "Guantes de gimnasio",
            descripcion:
                "Brindan mayor comodidad y protección al realizar ejercicios con peso.",
            categoria: "Accesorios",
            disponible: true,
            imagen: "imagenes/Guantes de gimnasio.png"
        },

        {
            id: 6,
            nombre: "Ropa deportiva",
            descripcion:
                "Prendas cómodas para entrenamientos en casa, gimnasio o espacios al aire libre.",
            categoria: "Ropa deportiva",
            disponible: false,
            imagen: "imagenes/Ropa deportiva.png"
        }

    ];


    // ==============================================
    // CREACIÓN DE MENSAJES PARA CADA CAMPO
    // ==============================================

    const errorNombre =
        crearMensajeCampo(
            nombreRegistro,
            "errorNombre"
        );

    const errorDescripcion =
        crearMensajeCampo(
            descripcionRegistro,
            "errorDescripcion"
        );

    const errorCategoria =
        crearMensajeCampo(
            categoriaRegistro,
            "errorCategoria"
        );


    function crearMensajeCampo(
        campo,
        idMensaje
    ) {

        let mensaje =
            document.getElementById(
                idMensaje
            );

        if (!mensaje) {

            mensaje =
                document.createElement(
                    "div"
                );

            mensaje.id =
                idMensaje;

            campo.insertAdjacentElement(
                "afterend",
                mensaje
            );

        }

        return mensaje;

    }


    // ==============================================
    // MOSTRAR ESTADO DE VALIDACIÓN
    // ==============================================

    function mostrarEstado(
        campo,
        contenedorMensaje,
        esValido,
        mensajeError,
        mensajeExito
    ) {

        campo.classList.remove(
            "is-valid",
            "is-invalid"
        );

        contenedorMensaje.classList.remove(
            "valid-feedback",
            "invalid-feedback",
            "d-block"
        );


        if (esValido) {

            campo.classList.add(
                "is-valid"
            );

            contenedorMensaje.classList.add(
                "valid-feedback",
                "d-block"
            );

            contenedorMensaje.textContent =
                mensajeExito;

        } else {

            campo.classList.add(
                "is-invalid"
            );

            contenedorMensaje.classList.add(
                "invalid-feedback",
                "d-block"
            );

            contenedorMensaje.textContent =
                mensajeError;

        }

    }


    // ==============================================
    // VALIDACIÓN DEL NOMBRE
    // ==============================================

    function validarNombre() {

        const nombre =
            nombreRegistro.value.trim();


        if (nombre === "") {

            mostrarEstado(
                nombreRegistro,
                errorNombre,
                false,
                "El nombre del producto es obligatorio.",
                ""
            );

            return false;

        }


        if (nombre.length < 3) {

            mostrarEstado(
                nombreRegistro,
                errorNombre,
                false,
                "El nombre debe tener mínimo 3 caracteres.",
                ""
            );

            return false;

        }


        mostrarEstado(
            nombreRegistro,
            errorNombre,
            true,
            "",
            "Nombre válido."
        );

        return true;

    }


    // ==============================================
    // VALIDACIÓN DE LA DESCRIPCIÓN
    // ==============================================

    function validarDescripcion() {

        const descripcion =
            descripcionRegistro.value.trim();


        if (descripcion === "") {

            mostrarEstado(
                descripcionRegistro,
                errorDescripcion,
                false,
                "La descripción es obligatoria.",
                ""
            );

            return false;

        }


        if (descripcion.length < 10) {

            mostrarEstado(
                descripcionRegistro,
                errorDescripcion,
                false,
                "La descripción debe tener mínimo 10 caracteres.",
                ""
            );

            return false;

        }


        mostrarEstado(
            descripcionRegistro,
            errorDescripcion,
            true,
            "",
            "Descripción válida."
        );

        return true;

    }


    // ==============================================
    // VALIDACIÓN DE LA CATEGORÍA
    // ==============================================

    function validarCategoria() {

        const categoria =
            categoriaRegistro.value;


        if (categoria === "") {

            mostrarEstado(
                categoriaRegistro,
                errorCategoria,
                false,
                "Debe seleccionar una categoría.",
                ""
            );

            return false;

        }


        mostrarEstado(
            categoriaRegistro,
            errorCategoria,
            true,
            "",
            "Categoría válida."
        );

        return true;

    }


    // ==============================================
    // VALIDAR TODO EL FORMULARIO
    // ==============================================

    function validarFormularioCompleto() {

        const nombreValido =
            validarNombre();

        const descripcionValida =
            validarDescripcion();

        const categoriaValida =
            validarCategoria();


        return (
            nombreValido &&
            descripcionValida &&
            categoriaValida
        );

    }


    // ==============================================
    // MOSTRAR MENSAJE GENERAL CON ALERTA BOOTSTRAP
    // ==============================================

    function mostrarMensajeGeneral(
        tipo,
        texto
    ) {

        mensajeValidacion.className = "";


        if (tipo === "exito") {

            mensajeValidacion.classList.add(
                "alert",
                "alert-success",
                "mt-3"
            );

        } else if (
            tipo === "advertencia"
        ) {

            mensajeValidacion.classList.add(
                "alert",
                "alert-warning",
                "mt-3"
            );

        } else {

            mensajeValidacion.classList.add(
                "alert",
                "alert-danger",
                "mt-3"
            );

        }


        mensajeValidacion.setAttribute(
            "role",
            "alert"
        );

        mensajeValidacion.textContent =
            texto;

    }


    // ==============================================
    // OBTENER IMAGEN SEGÚN EL NOMBRE DEL PRODUCTO
    // ==============================================

    function obtenerImagenProducto(
        nombre
    ) {

        const nombreNormalizado =
            nombre
                .trim()
                .toLowerCase();


        const imagenesProductos = {

            "bandas elásticas":
                "imagenes/Bandas elásticas.png",

            "bandas elasticas":
                "imagenes/Bandas elásticas.png",

            "mancuernas":
                "imagenes/mancuernas.png",

            "colchonetas":
                "imagenes/Colchonetas.png",

            "botellas deportivas":
                "imagenes/Botellas deportivas.png",

            "guantes de gimnasio":
                "imagenes/Guantes de gimnasio.png",

            "ropa deportiva":
                "imagenes/Ropa deportiva.png"

        };


        return (
            imagenesProductos[
                nombreNormalizado
            ] || ""
        );

    }


    // ==============================================
    // REGISTRAR UN NUEVO PRODUCTO
    // ==============================================

    function registrarProducto() {

        const nuevoProducto = {

            id:
                Date.now(),

            nombre:
                nombreRegistro
                    .value
                    .trim(),

            descripcion:
                descripcionRegistro
                    .value
                    .trim(),

            categoria:
                categoriaRegistro
                    .value,

            disponible:
                true,

            imagen:
                obtenerImagenProducto(
                    nombreRegistro.value
                )

        };


        productos.push(
            nuevoProducto
        );


        mostrarProductos();

        actualizarContador();


        mostrarMensajeGeneral(
            "exito",
            "Producto registrado correctamente."
        );


        formulario.reset();

        limpiarValidaciones();

    }


    // ==============================================
    // MOSTRAR PRODUCTOS DINÁMICAMENTE
    // ==============================================

    function mostrarProductos() {

        contenedorProductos.innerHTML =
            "";


        // Condición cuando no existen productos
        if (
            productos.length === 0
        ) {

            contenedorProductos.innerHTML = `

                <div class="col-12">

                    <div
                        class="alert alert-warning text-center"
                        role="alert"
                    >
                        Aún no se han registrado
                        productos deportivos.
                    </div>

                </div>

            `;

            return;

        }


        // Estructura repetitiva para mostrar productos
        productos.forEach(
            function (producto) {

                // ==============================================
                // COLUMNA BOOTSTRAP
                // ==============================================

                const columna =
                    document.createElement(
                        "article"
                    );

                columna.className =
                    "col-sm-12 col-md-6 col-lg-4 mb-4";


                // ==============================================
                // TARJETA BOOTSTRAP
                // ==============================================

                const tarjeta =
                    document.createElement(
                        "div"
                    );

                tarjeta.className =
                    "card h-100 shadow-sm";


                // ==============================================
                // IMAGEN DEL PRODUCTO
                // ==============================================

                if (
                    producto.imagen
                ) {

                    const imagenProducto =
                        document.createElement(
                            "img"
                        );

                    imagenProducto.src =
                        producto.imagen;

                    imagenProducto.alt =
                        "Imagen de " +
                        producto.nombre;

                    imagenProducto.className =
                        "card-img-top imagen-producto";

                    tarjeta.appendChild(
                        imagenProducto
                    );

                }


                // ==============================================
                // CUERPO DE LA TARJETA
                // ==============================================

                const cuerpoTarjeta =
                    document.createElement(
                        "div"
                    );

                cuerpoTarjeta.className =
                    "card-body text-center d-flex flex-column";


                // ==============================================
                // NOMBRE DEL PRODUCTO
                // ==============================================

                const nombreProducto =
                    document.createElement(
                        "h3"
                    );

                nombreProducto.className =
                    "card-title";

                nombreProducto.textContent =
                    producto.nombre;


                // ==============================================
                // DESCRIPCIÓN
                // ==============================================

                const descripcionProducto =
                    document.createElement(
                        "p"
                    );

                descripcionProducto.className =
                    "card-text flex-grow-1";

                descripcionProducto.textContent =
                    producto.descripcion;


                // ==============================================
                // CATEGORÍA
                // ==============================================

                const categoriaProducto =
                    document.createElement(
                        "span"
                    );

                categoriaProducto.className =
                    "badge bg-primary mb-2";

                categoriaProducto.textContent =
                    producto.categoria;


                // ==============================================
                // ESTADO
                // ==============================================

                const estadoProducto =
                    document.createElement(
                        "span"
                    );


                if (
                    producto.disponible
                ) {

                    estadoProducto.className =
                        "badge bg-success mb-3";

                    estadoProducto.textContent =
                        "Disponible";

                } else {

                    estadoProducto.className =
                        "badge bg-danger mb-3";

                    estadoProducto.textContent =
                        "Agotado";

                }


                // ==============================================
                // CONTENEDOR DE BOTONES
                // ==============================================

                const contenedorBotones =
                    document.createElement(
                        "div"
                    );

                contenedorBotones.className =
                    "d-flex gap-2 justify-content-center mt-auto";


                // ==============================================
                // BOTÓN VER DETALLES
                // ==============================================

                const botonDetalles =
                    document.createElement(
                        "button"
                    );

                botonDetalles.type =
                    "button";

                botonDetalles.className =
                    "btn btn-primary btn-sm btn-detalles";

                botonDetalles.setAttribute(
                    "data-id",
                    producto.id
                );

                botonDetalles.textContent =
                    "Ver detalles";


                // ==============================================
                // BOTÓN ELIMINAR
                // ==============================================

                const botonEliminar =
                    document.createElement(
                        "button"
                    );

                botonEliminar.type =
                    "button";

                botonEliminar.className =
                    "btn btn-danger btn-sm btn-eliminar";

                botonEliminar.setAttribute(
                    "data-id",
                    producto.id
                );

                botonEliminar.textContent =
                    "Eliminar";


                // ==============================================
                // AGREGAR BOTONES
                // ==============================================

                contenedorBotones.appendChild(
                    botonDetalles
                );

                contenedorBotones.appendChild(
                    botonEliminar
                );


                // ==============================================
                // AGREGAR CONTENIDO A LA TARJETA
                // ==============================================

                cuerpoTarjeta.appendChild(
                    nombreProducto
                );

                cuerpoTarjeta.appendChild(
                    descripcionProducto
                );

                cuerpoTarjeta.appendChild(
                    categoriaProducto
                );

                cuerpoTarjeta.appendChild(
                    estadoProducto
                );

                cuerpoTarjeta.appendChild(
                    contenedorBotones
                );


                tarjeta.appendChild(
                    cuerpoTarjeta
                );

                columna.appendChild(
                    tarjeta
                );

                contenedorProductos.appendChild(
                    columna
                );

            }
        );

    }


    // ==============================================
    // MOSTRAR DETALLES DEL PRODUCTO EN EL MODAL
    // ==============================================

    function mostrarDetallesProducto(
        id
    ) {

        const productoEncontrado =
            productos.find(
                function (producto) {

                    return (
                        producto.id === id
                    );

                }
            );


        if (
            !productoEncontrado
        ) {

            mostrarMensajeGeneral(
                "error",
                "No fue posible encontrar el producto."
            );

            return;

        }


        // Verificar que el modal exista en el HTML
        if (
            !modalProducto ||
            !modalTitulo ||
            !modalDescripcion ||
            !modalCategoria ||
            !modalEstado
        ) {

            mostrarMensajeGeneral(
                "error",
                "No fue posible abrir los detalles del producto."
            );

            return;

        }


        modalTitulo.textContent =
            productoEncontrado.nombre;


        modalDescripcion.textContent =
            productoEncontrado.descripcion;


        modalCategoria.textContent =
            productoEncontrado.categoria;


        modalEstado.textContent =
            productoEncontrado.disponible
                ? "Disponible"
                : "Agotado";


        if (
            productoEncontrado.disponible
        ) {

            modalEstado.className =
                "badge bg-success";

        } else {

            modalEstado.className =
                "badge bg-danger";

        }


        // ==============================================
        // IMAGEN DEL MODAL
        // ==============================================

        if (
            modalImagen
        ) {

            if (
                productoEncontrado.imagen
            ) {

                modalImagen.src =
                    productoEncontrado.imagen;

                modalImagen.alt =
                    "Imagen de " +
                    productoEncontrado.nombre;

                modalImagen.classList.remove(
                    "d-none"
                );

            } else {

                modalImagen.classList.add(
                    "d-none"
                );

            }

        }


        // ==============================================
        // ABRIR MODAL BOOTSTRAP
        // ==============================================

        if (
            typeof bootstrap !==
            "undefined"
        ) {

            const instanciaModal =
                bootstrap.Modal
                    .getOrCreateInstance(
                        modalProducto
                    );

            instanciaModal.show();

        } else {

            mostrarMensajeGeneral(
                "error",
                "Bootstrap no se ha cargado correctamente."
            );

        }

    }


    // ==============================================
    // ACTUALIZAR CONTADOR DE PRODUCTOS
    // ==============================================

    function actualizarContador() {

        totalRegistros.textContent =
            productos.length;

    }


    // ==============================================
    // ELIMINAR PRODUCTO
    // ==============================================

    function eliminarProducto(
        id
    ) {

        const productoEncontrado =
            productos.find(
                function (producto) {

                    return (
                        producto.id === id
                    );

                }
            );


        productos =
            productos.filter(
                function (producto) {

                    return (
                        producto.id !== id
                    );

                }
            );


        mostrarProductos();

        actualizarContador();


        if (
            productoEncontrado
        ) {

            mostrarMensajeGeneral(
                "exito",
                `El producto "${productoEncontrado.nombre}" fue eliminado correctamente.`
            );

        }

    }


    // ==============================================
    // LIMPIAR VALIDACIONES VISUALES
    // ==============================================

    function limpiarValidaciones() {

        nombreRegistro.classList.remove(
            "is-valid",
            "is-invalid"
        );


        descripcionRegistro.classList.remove(
            "is-valid",
            "is-invalid"
        );


        categoriaRegistro.classList.remove(
            "is-valid",
            "is-invalid"
        );


        errorNombre.textContent =
            "";

        errorDescripcion.textContent =
            "";

        errorCategoria.textContent =
            "";


        errorNombre.className =
            "";

        errorDescripcion.className =
            "";

        errorCategoria.className =
            "";

    }


    // ==============================================
    // MOSTRAR SPINNER
    // ==============================================

    function mostrarSpinner() {

        if (
            spinnerCarga
        ) {

            spinnerCarga.classList.remove(
                "d-none"
            );

        }

    }


    // ==============================================
    // OCULTAR SPINNER
    // ==============================================

    function ocultarSpinner() {

        if (
            spinnerCarga
        ) {

            spinnerCarga.classList.add(
                "d-none"
            );

        }

    }


    // ==============================================
    // EVENTOS DE VALIDACIÓN EN TIEMPO REAL
    // ==============================================

    nombreRegistro.addEventListener(
        "input",
        validarNombre
    );


    descripcionRegistro.addEventListener(
        "input",
        validarDescripcion
    );


    categoriaRegistro.addEventListener(
        "change",
        validarCategoria
    );


    nombreRegistro.addEventListener(
        "blur",
        validarNombre
    );


    descripcionRegistro.addEventListener(
        "blur",
        validarDescripcion
    );


    categoriaRegistro.addEventListener(
        "blur",
        validarCategoria
    );


    // ==============================================
    // EVENTO SUBMIT DEL FORMULARIO
    // ==============================================

    formulario.addEventListener(
        "submit",
        function (evento) {

            evento.preventDefault();


            if (
                validarFormularioCompleto()
            ) {

                mostrarSpinner();


                mostrarMensajeGeneral(
                    "advertencia",
                    "Procesando el registro del producto..."
                );


                // Simulación de proceso de carga
                setTimeout(
                    function () {

                        registrarProducto();

                        ocultarSpinner();

                    },
                    1200
                );

            } else {

                mostrarMensajeGeneral(
                    "error",
                    "Por favor, corrija los campos marcados antes de registrar el producto."
                );

            }

        }
    );


    // ==============================================
    // EVENTOS DE LOS PRODUCTOS
    // ==============================================

    contenedorProductos.addEventListener(
        "click",
        function (evento) {


            // ==============================================
            // BOTÓN ELIMINAR
            // ==============================================

            if (
                evento.target.classList.contains(
                    "btn-eliminar"
                )
            ) {

                const idProducto =
                    Number(
                        evento.target.getAttribute(
                            "data-id"
                        )
                    );


                eliminarProducto(
                    idProducto
                );

            }


            // ==============================================
            // BOTÓN VER DETALLES
            // ==============================================

            if (
                evento.target.classList.contains(
                    "btn-detalles"
                )
            ) {

                const idProducto =
                    Number(
                        evento.target.getAttribute(
                            "data-id"
                        )
                    );


                mostrarDetallesProducto(
                    idProducto
                );

            }

        }
    );


    // ==============================================
    // CARGA INICIAL DE LOS PRODUCTOS
    // ==============================================

    mostrarProductos();

    actualizarContador();

    ocultarSpinner();

});
