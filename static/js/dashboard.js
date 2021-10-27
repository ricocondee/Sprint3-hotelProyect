/**Show dash */
const showdash = (toggleId, navbarId) => {
    const toggle = document.getElementById(toggleId),
    navbar = document.getElementById(navbarId);
    
    if (toggle && navbar){
        toggle.addEventListener('click', ()=>{
            navbar.classList.toggle('show-dash')
        });
    }
}
showdash('side_nav__toggle','side__navbar')
