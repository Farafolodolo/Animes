//When the document is ready, it will activate a materialize function for the selects (that makes the selects look better)
$(document).ready(function(){ $('select').formSelect(); });

//The currentPage (It will be increasing while the user is going down)
let currentPage = 1;
//Boolean variable to know if the next animes are loading
let isLoading = false;
//Boolean variabe to know if there are more animes in the database to show
let has_next_loading = false;

//Functions to make the loader show up or hide
function showLoader() { document.getElementById('loader').style.display = 'block'; }
function hideLoader() { document.getElementById('loader').style.display = 'none'; }

//Function to load the animes, it states the reset like false as default
async function loadAnimes(reset = false) {
    //if is loading it won't allow to duplicate the requests
    if(isLoading) return;
    //Changes the variable
    isLoading = true;
    //It shows the loader
    showLoader();
    //If the variable reset is true, is going to start again from the page 1
    if(reset) currentPage = 1;

    //It creates an object to send the args 
    const params = new URLSearchParams({
    search: document.getElementById('search').value,
    year: document.querySelector('[name="year"]').value,
    //Query selector is more flexible than the get element by id (If I am honest, I would have used get element by id, but the man in the tutorial did it in this way)
    season: document.querySelector('[name="season"]').value,
    format: document.querySelector('[name="format"]').value,
    status: document.querySelector('[name="status"]').value,
    genre: document.querySelector('[name="genre"]').value,
    page: currentPage
    });

    try {
    //It makes a request to the api with the args stated on top
    const response = await fetch(`/api/animes?${params.toString()}`);
    //It converts the response from JSON to an javascript object
    const data = await response.json();
    //If reset is true, it's going to clean the anime container by replacing all the content with a ''
    if(reset) document.getElementById('anime-container').innerHTML = '';
    //If there are not results, It's going to show the display
    if(data.animes.length === 0 && currentPage === 1) {
        document.getElementById('no-results').style.display = 'block';
    } else {
        document.getElementById('no-results').style.display = 'none';
    }
    //It's going to iterate all the animes and adding a index for the animation for showing up
    data.animes.forEach((anime, index) => {
        //It creates a list of genres coming from the response
        const genresList = Array.isArray(anime.genres) 
        //The slice is for selecting the first three genres, map is for creating a completely new array adding elements of the original array, and the join for literally joining all the elements on the array
        ? anime.genres.slice(0, 3).map(genre => `<span class="genre-tag">${genre}</span>`).join('')
        //If there is not anything, it will return a void value 
        : '';
        
        //This part adds a badge depending of the situation (currently airing or movie)
        const statusBadge = anime.airing_status === 'Currently Airing' 
        ? '<span class="badge airing">Currently Airing</span>' 
        : anime.format_type === 'Movie' 
            ? '<span class="badge movie">Movie</span>' 
            : '';
        //It creates the card with HTML and adding the different variables on the information
        const card = `
        <a href="/specific_anime/${anime.id}">
        <div class="anime-card" style="--animation-order: ${index}">
            ${statusBadge}
            <div class="card-image">
            <img src="${anime.image_url}" alt="${anime.title}" loading="lazy">
            <div class="anime-info-overlay">
                <div class="info-item"><strong>Status:</strong> ${anime.airing_status}</div>
                <div class="info-item"><strong>Type:</strong> ${anime.format_type}</div>
                <div class="info-item"><strong>Season:</strong> ${anime.season || 'N/A'}</div>
                <div class="info-item"><strong>Episodes:</strong> ${anime.episodes || 'Desconocido'}</div>
                <div class="info-item"><strong>Genres:</strong></div>
                <div class="genre-tags">${genresList}</div>
            </div>
            </div>
            <div class="anime-title truncate">${anime.title}</div>
        </div>
        </a>
        `;
        //It inserts the card on the container, the before is for adding it at the end
        document.getElementById('anime-container').insertAdjacentHTML('beforeend', card);
    });
    //if there are more animes to show, will increase by one the current page and has next loading will be true
    if(data.has_next){
        currentPage++;
        has_next_loading = true
    } else{
        has_next_loading = false
    }

    } catch(error) {
    console.error('Error:', error);
    } finally {
    //After all the instruction, it will hide the loader and change the variable isLoading to false (for allowing adding more animes)
    hideLoader();
    isLoading = false;
    }
}

// It manage the scroll on the window, scrollTop is the current position, scrollHeight is the height of all the content, and the clientHeight is the visible height to the user
window.addEventListener('scroll', () => {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    //If the user is approaching to the end, and is not loading, and there are more animes to show up, it will call the function loadAnimes
    if (scrollTop + clientHeight >= scrollHeight - 600 && !isLoading && has_next_loading) {
    loadAnimes();
    }
    
    // If the current scrollTop is more than 300, it will show up the button to return at the beggining of the page
    if (scrollTop > 300) {
    document.getElementById('scroll-top').classList.add('visible');
    } else {
    document.getElementById('scroll-top').classList.remove('visible');
    }
});

// If the user presses the button, it will return the user to the beggining with a good animation
document.getElementById('scroll-top').addEventListener('click', () => {
    window.scrollTo({
    top: 0,
    behavior: 'smooth'
    });
});

// If the user is typing on the input search it will activate the function loadAnimes with the reset true
document.getElementById('search').addEventListener('input', () => loadAnimes(true));

// It cleans the container when the user presses the html with the class close or input-field
document.querySelector('.input-field .close').addEventListener('click', () => {
    document.getElementById('search').value = '';
    loadAnimes(true);
});

//It detects if the user presses the enter button on the search (activating the function loadAnimes)
document.getElementById('search').addEventListener('keydown', () => {
    if (event.key === 'Enter' || event.keyCode === 13){
    loadAnimes(true)
    }
    })

// It takes all the selects and detects if there is a change on them, if that's true it will activate the function loadAnimes with the reset true
document.querySelectorAll('select').forEach(select => {
    select.addEventListener('change', () => loadAnimes(true));
});

// It loads the first animes
loadAnimes();