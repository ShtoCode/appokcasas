const contactos = JSON.parse(localStorage.getItem("contactos")) || [];
const form = document.getElementById("contacto-form");
window.onload = () => {
  form.onsubmit = (e) => {
    e.preventDefault();

    const nombre = document.getElementById("nombre").value;
    const apellido = document.getElementById("apellido").value;
    const email = document.getElementById("email").value;
    const mensaje = document.getElementById("mensaje-contacto").value;

    validarFormulario();

    function validarFormulario() {
      if (nombre.length == 0) {
        swal({
          title: "Error!",
          text: "El campo nombre está vacio",
          icon: "error",
        });
      } if (apellido.length == 0) {
        swal({
          title: "Error!",
          text: "El campo apellido está vacio",
          icon: "error",
        });
      } if (email.length == 0) {
        swal({
          title: "Error!",
          text: "El campo email está vacio",
          icon: "error",
        });
      } if (mensaje.length == 0) {
        swal({
          title: "Error!",
          text: "El campo mensaje está vacio",
          icon: "error",
        });
      } else {
        contactos.push(nombre, apellido, email, mensaje);
        const contactoValue = JSON.stringify(contactos);
        localStorage.setItem("contactos", contactoValue)
        swal({
          title: "Contacto enviado",
          text: "El formulario ha sido enviado, gracias por contactarnos!",
          icon: "success",
        });
      }
    }
  };
};
