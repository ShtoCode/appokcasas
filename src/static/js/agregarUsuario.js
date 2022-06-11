const form = document.getElementById("registro-form");
window.onload = () => {
  form.onsubmit = (e) => {
    e.preventDefault();
    const nombre = document.getElementById("nombre").value;
    const apellido = document.getElementById("apellido").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    validarForm();

    async function validarForm() {
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
        const response = await fetch("/registrar", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            nombre,
            apellido,
            email,
            password,
          }),
        });

        const data = await response;
        console.log(data);

        swal({
          title: "Usuario registrado!",
          text: "El usuario ha sido registrado con exito.",
          icon: "success",
        }).then(function (){
            window.location.href = 'login'
        });
      }
    }
    form.reset();
  };
};
