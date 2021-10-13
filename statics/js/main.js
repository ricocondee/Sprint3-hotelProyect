/*======================= SHOW MENU =============================== */
const showMenu = (toggleId, navId) =>{
    /**
     * los datos de los ID son asignados a las variables "toggle" y "nav"
     */
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId);
    /**
     * Con un condicional "if" se crea un event listener pala toggle (icono de menú)
     */
    // Validate that variables exist
    if(toggle && nav){
        toggle.addEventListener('click', ()=>{
            /**
             * Añade las propiedades "show-menu"  => (File: _header.scss)
             * al elemento con el class "nav__menu" permitiendo que el menú
             * sea desplazado de arriba hacia abajo.
             **/ 

            nav.classList.toggle('show-menu')
        })
    }
}
/**
 * Inicializo la función capturando las etiquetas:
 *  1) nav-toggle => que contiene el icono grid que hace referencia al menú
 *  2) nav-menu => que contiene las opciones a seleccionar del menu
 */
showMenu('nav-toggle','nav-menu') 

/*===================== REMOVE MENU MOBILE ====================== */
/* Quita el menú una vez se haya seleccionado una opción */


const navLink = document.querySelectorAll('.nav__link') 

function linkAction(){
    const navMenu = document.getElementById('nav-menu')
    // When we click on each nav__link, we remove the show-menu class
    navMenu.classList.remove('show-menu')
}

/**
 * Añado un evento que está al tanto cuando un elemento del menú es seleccionado
 * al realizar un "click" se ejecuta la funcion "linkAction" que se 
 * encarga de remover el elemento "show-menu"
 */
navLink.forEach(n => n.addEventListener('click', linkAction))

/*=========================== SWIPER SLIDE ===========================*/
let swiper = new Swiper('.oferta__container', {
    cssMode: true,
    loop: true,

    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    mousewheel: true,
    keyboard: true,

});