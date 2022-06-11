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

    const lblInstalaciones =
      document.getElementById("lblInstalaciones").textContent;
    const lblMetros = document.getElementById("lblMetros").textContent;
    const lblLuz = document.getElementById("lblLuz").textContent;
    const lblTermografia =
      document.getElementById("lblTermografia").textContent;


    const valorInstalaciones = document.getElementById('valorInstalaciones').textContent
    const valorMetros = document.getElementById('valorMetros').textContent
    const valorLuz = document.getElementById('valorLuz').textContent
    const valorTermografia = document.getElementById('valorTermografia').textContent

    console.log(lblInstalaciones);
    console.log(lblMetros);
    console.log(lblLuz);
    console.log(lblTermografia);

    validarForm();
    async function validarForm() {
      if (
        instalacionesVal == false &&
        metrosVal == false &&
        luzVal == false &&
        termografiaVal == false
      ) {
        swal({
          title: "Error!",
          text: "No ha seleccionado ningún servicio",
          icon: "error",
        });
      }

      if (instalacionesVal == true) {
        const response = await fetch("/servicios", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            lblInstalaciones,
            instalacionesVal,
            metrosVal,
            luzVal,
            termografiaVal,
            valorInstalaciones
          }),
        });
        swal({
          title: 'Servicios agregados!',
          text: 'Los servicios seleccionados han sido agregados correctamente.',
          icon: 'success'
        }) 
        
        const data = await response;
        console.log(data);
      } 
      
       if (metrosVal == true) {
        const response = await fetch("/servicios", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            lblMetros,
            metrosVal,
            instalacionesVal,
            luzVal,
            termografiaVal,
            valorMetros
          }),
        });
        swal({
          title: 'Servicios agregados!',
          text: 'Los servicios seleccionados han sido agregados correctamente.',
          icon: 'success'
        }) 
        
        const data = await response;
        console.log(data);
      }     
      
      if (luzVal == true) {
        const response = await fetch("/servicios", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            lblLuz,
            luzVal, 
            instalacionesVal,
            metrosVal,
            termografiaVal,
            valorLuz
          }),
        });
        swal({
          title: 'Servicios agregados!',
          text: 'Los servicios seleccionados han sido agregados correctamente.',
          icon: 'success'
        }) 
        
        const data = await response;
        console.log(data);
      }          
      
      if (termografiaVal == true) {
        const response = await fetch("/servicios", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            lblTermografia,
            termografiaVal,
            instalacionesVal,
            metrosVal,
            luzVal,
            valorTermografia
          }),
        }); 
        swal({
          title: 'Servicios agregados!',
          text: 'Los servicios seleccionados han sido agregados correctamente.',
          icon: 'success'
        })
        
        const data = await response;
        console.log(data);
      }
            
      
    }

    form.reset();
  };
};
