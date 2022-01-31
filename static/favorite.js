const favorited = document.querySelector("#red-heart")
const notFavorite = document.querySelector("#white-heart")

if (favorited) {
    favorited.addEventListener("click", function() {
        console.log("red-heart")
    })
}

if (notFavorite) {
    notFavorite.addEventListener("click", function() {
        console.log("white-heart")
    })
}
