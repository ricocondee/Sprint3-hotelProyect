const effect = document.getElementById('swipe-effect')
const formLogin = document.getElementById('swipe-one')
const formRegister = document.getElementById('swipe-two')
const route = window.location.href.indexOf('/signup')

effect.addEventListener('click', function() {

    if (formLogin.classList.contains('swipe-one')){
        formLogin.classList.remove('swipe-one')
    }
    else{
        formLogin.classList.add('swipe-one')
    }

    if (formRegister.classList.contains('swipe-two')){
        formRegister.classList.remove('swipe-one')
    }
    else{
        formRegister.classList.add('swipe-two')
    }

    if (this.textContent == "Log In"){
        this.textContent = "Sign Up"
    }
    else{
        this.textContent = "Log In"
    }
});

if (route != -1){
    formLogin.classList.add('swipe-one')
    formRegister.classList.add('swipe-two')
}
