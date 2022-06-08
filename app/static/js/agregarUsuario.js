const usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];
const form = document.getElementById("registro-form");

window.onload = () => {
  form.onsubmit = (e) => {
    e.preventDefault();
    const nombre = document.getElementById("nombre").value;
    const apellido = document.getElementById("apellido").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    validarForm();

    function validarForm() {
      if (nombre.length == 0) {
        swal({
          title: "Error!",
          text: "El campo nombre no puede estar vacio.",
          icon: "error",
        });
      }
      if (apellido.length == 0) {
        swal({
          title: "Error!",
          text: "El campo apellido no puede estar vacio.",
          icon: "error",
        });
      }
      if (email.length == 0) {
        swal({
          title: "Error!",
          text: "El campo email no puede estar vacio.",
          icon: "error",
        });
      }
      if (password.length == 0) {
        swal({
          title: "Error!",
          text: "El campo password no puede estar vacio.",
          icon: "error",
        });
      } else {
        usuarios.push(nombre, apellido, email, password);
        const usuarioValue = JSON.stringify(usuarios);
        localStorage.setItem("usuarios", usuarioValue);
        swal({
          title: "Usuario registrado!",
          text: "El usuario ha sido registrado con exito.",
          icon: "success"
        });
      }
    }
  };
};
