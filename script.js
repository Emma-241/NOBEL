document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const container = document.getElementById("container");

    // Fonction pour afficher le formulaire de connexion
    function showLoginForm() {
        container.classList.add("show-login");
        container.classList.remove("show-register");
    }

    // Fonction pour afficher le formulaire d'inscription (facultatif)
    function showRegisterForm() {
        container.classList.add("show-register");
        container.classList.remove("show-login");
        alert("La fonctionnalité 'S'inscrire' est en cours de développement.");
    }

    // Événement pour le bouton "Connexion"
    document.querySelector(".nav-button").addEventListener("click", showLoginForm);

    // Événement pour le bouton "S'inscrire" (facultatif)
    document.querySelectorAll(".nav-button")[1].addEventListener("click", showRegisterForm);

    // Optionnel : Gestion de la soumission du formulaire de connexion
    loginForm.addEventListener("submit", (e) => {
        e.preventDefault(); // Empêcher l'envoi du formulaire pour démonstration
        // Récupérer les valeurs des champs
        const username = loginForm.username.value;
        const password = loginForm.password.value;

        // Exemple de traitement simple (remplacez cette partie par votre logique d'authentification)
        if (username && password) {
            alert(Connexion réussie pour l'utilisateur : ${username});
            // Redirection ou logique supplémentaire ici
        } else {
            alert("Veuillez entrer une adresse mail et un mot de passe valides.");
        }
    });
});