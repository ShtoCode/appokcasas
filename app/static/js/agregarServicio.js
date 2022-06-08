const servicios = JSON.parse(localStorage.getItem("servicios")) || [];
const form = document.getElementById("servicios-form");
window.onload = () => {
  form.onsubmit = (e) => {
    e.preventDefault();
    const instalaciones = document.getElementById("instalaciones");
    const metros = document.getElementById("metros");
    const luz = document.getElementById("luz");
    const termografia = document.getElementById("termografia");
    const instalacionesVal = instalaciones.checked;
    const metrosVal = metros.checked;
    const luzVal = luz.checked;
    const termografiaVal = termografia.checked;

    validarForm();
    function validarForm() {
      if (
        instalacionesVal == false &&
        metrosVal == false &&
        luzVal == false &&
        termografiaVal == false
      ) {
          swal({
            title:'Error!',
            text:'No ha seleccionado ningún servicio',
            icon:'error'
        })
      } else {
        servicios.push(instalacionesVal, metrosVal, luzVal, termografiaVal);
        const serviciosValue = JSON.stringify(servicios);
        localStorage.setItem("servicios", serviciosValue);
        swal({
          title:'Servicios agregados!',
          text:'Los servicios seleccionados han sido agregados correctamente.',
          icon:'success'
        })
      }
    }

  };
};
