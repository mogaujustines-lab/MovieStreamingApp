const fallbackMovies = [
  {
    id: 1,
    title: 'The Dark Knight',
    genre: 'Action',
    genres: 'Action|Crime|Drama',
    year: 2008,
    rating: 9.0,
    director: 'Christopher Nolan',
    cast: ['Christian Bale', 'Heath Ledger', 'Aaron Eckhart'],
    keywords: ['batman', 'gotham', 'crime', 'hero'],
    description: 'Batman faces a criminal mastermind who turns Gotham into a living nightmare.',
    poster: 'https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 2,
    title: 'Batman Begins',
    genre: 'Action',
    genres: 'Action|Crime|Drama',
    year: 2005,
    rating: 8.2,
    director: 'Christopher Nolan',
    cast: ['Christian Bale', 'Michael Caine', 'Liam Neeson'],
    keywords: ['batman', 'gotham', 'origin', 'hero'],
    description: 'A billionaire adopts the guise of a vigilante to fight crime in Gotham.',
    poster: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 3,
    title: 'Inception',
    genre: 'Sci-Fi',
    genres: 'Sci-Fi|Action|Thriller',
    year: 2010,
    rating: 8.8,
    director: 'Christopher Nolan',
    cast: ['Leonardo DiCaprio', 'Joseph Gordon-Levitt', 'Tom Hardy'],
    keywords: ['dream', 'mind', 'action', 'heist'],
    description: 'A thief enters dreams to plant an idea in a target mind and change a company.',
    poster: 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 4,
    title: 'Joker',
    genre: 'Drama',
    genres: 'Drama|Crime|Thriller',
    year: 2019,
    rating: 8.4,
    director: 'Todd Phillips',
    cast: ['Joaquin Phoenix', 'Robert De Niro', 'Zazie Beetz'],
    keywords: ['madness', 'society', 'crime', 'chaos'],
    description: 'A troubled comedian spirals into chaos as he becomes the symbol of rebellion.',
    poster: 'https://images.unsplash.com/photo-1497032628192-86f99bcd76bc?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 5,
    title: 'Interstellar',
    genre: 'Sci-Fi',
    genres: 'Sci-Fi|Adventure|Drama',
    year: 2014,
    rating: 8.7,
    director: 'Christopher Nolan',
    cast: ['Matthew McConaughey', 'Anne Hathaway', 'Jessica Chastain'],
    keywords: ['space', 'time', 'exploration', 'future'],
    description: 'A team of astronauts ventures across galaxies to find a new home for humanity.',
    poster: 'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 6,
    title: 'The Avengers',
    genre: 'Action',
    genres: 'Action|Adventure|Sci-Fi',
    year: 2012,
    rating: 8.0,
    director: 'Joss Whedon',
    cast: ['Robert Downey Jr.', 'Chris Evans', 'Scarlett Johansson'],
    keywords: ['superhero', 'team', 'battle', 'marvel'],
    description: 'The world’s greatest heroes unite to stop an alien invasion threatening Earth.',
    poster: 'https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 7,
    title: 'Dune',
    genre: 'Adventure',
    genres: 'Adventure|Sci-Fi|Action',
    year: 2021,
    rating: 8.1,
    director: 'Denis Villeneuve',
    cast: ['Timothée Chalamet', 'Rebecca Ferguson', 'Oscar Isaac'],
    keywords: ['desert', 'power', 'empire', 'future'],
    description: 'A noble family becomes entangled in the struggle for control of a desert planet.',
    poster: 'https://images.unsplash.com/photo-1513106580091-1d82408b8cd6?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 8,
    title: 'Parasite',
    genre: 'Thriller',
    genres: 'Thriller|Drama|Mystery',
    year: 2019,
    rating: 8.5,
    director: 'Bong Joon-ho',
    cast: ['Song Kang-ho', 'Lee Sun-kyun', 'Cho Yeo-jeong'],
    keywords: ['class', 'family', 'dark', 'twist'],
    description: 'A poor family infiltrates a wealthy household and the tension escalates quickly.',
    poster: 'https://images.unsplash.com/photo-1608889825103-eb5ed706fc64?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 9,
    title: 'The Matrix',
    genre: 'Sci-Fi',
    genres: 'Sci-Fi|Action',
    year: 1999,
    rating: 8.7,
    director: 'The Wachowskis',
    cast: ['Keanu Reeves', 'Laurence Fishburne', 'Carrie-Anne Moss'],
    keywords: ['simulation', 'reality', 'cyber', 'future'],
    description: 'A hacker discovers the world is a constructed simulation and joins the resistance.',
    poster: 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 10,
    title: 'The Prestige',
    genre: 'Drama',
    genres: 'Drama|Mystery|Thriller',
    year: 2006,
    rating: 8.5,
    director: 'Christopher Nolan',
    cast: ['Hugh Jackman', 'Christian Bale', 'Scarlett Johansson'],
    keywords: ['magic', 'rivalry', 'obsession', 'twist'],
    description: 'Two magicians become rivals in a contest of illusion and sacrifice.',
    poster: 'https://images.unsplash.com/photo-1516280440614-37939bbacd81?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 11,
    title: 'Mad Max: Fury Road',
    genre: 'Action',
    genres: 'Action|Adventure|Sci-Fi',
    year: 2015,
    rating: 8.1,
    director: 'George Miller',
    cast: ['Tom Hardy', 'Charlize Theron', 'Nicholas Hoult'],
    keywords: ['road', 'chaos', 'survival', 'rebellion'],
    description: 'A lone drifter joins a rebel leader in a high-speed race across the desert.',
    poster: 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=700&q=80'
  },
  {
    id: 12,
    title: 'Arrival',
    genre: 'Sci-Fi',
    genres: 'Sci-Fi|Drama|Mystery',
    year: 2016,
    rating: 7.9,
    director: 'Denis Villeneuve',
    cast: ['Amy Adams', 'Jeremy Renner', 'Forest Whitaker'],
    keywords: ['language', 'aliens', 'communication', 'time'],
    description: 'A linguist attempts to communicate with extraterrestrial visitors before time runs out.',
    poster: 'https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?auto=format&fit=crop&w=700&q=80'
  }
];

let movies = [...fallbackMovies];

const state = {
  query: '',
  genre: 'All',
  year: 'All',
  rating: 'All',
  selectedMovie: movies[0],
  favorites: new Set(),
  userRatings: {},
  newUser: true,
  displayName: 'New User',
  user: null
};

const trendingList = document.getElementById('trendingList');
const recommendedList = document.getElementById('recommendedList');
const filterInput = document.getElementById('searchInput');
const filterInputSecondary = document.getElementById('searchInputSecondary');
const genreFilter = document.getElementById('genreFilter');
const yearFilter = document.getElementById('yearFilter');
const ratingFilter = document.getElementById('ratingFilter');
const modal = document.getElementById('movieModal');
const modalDetails = document.getElementById('modalDetails');
const authModal = document.getElementById('authModal');
const authForm = document.getElementById('authForm');

let authMode = 'login';
let recommendationRequestId = 0;
let recommendationTimer = null;

function posterFallback(movie) {
  const palettes = [
    ['#122b3a', '#e86c4f'],
    ['#32233b', '#f3a24b'],
    ['#142b4d', '#7ac8db'],
    ['#321d24', '#e55368']
  ];

  const palette = palettes[(Number(movie.id) - 1) % palettes.length];
  const title = String(movie.title || 'Movie')
    .replace(/[&<>"']/g, ' ')
    .slice(0, 24);

  const genre = String(movie.genre || 'FEATURE')
    .replace(/[&<>"']/g, ' ')
    .toUpperCase()
    .slice(0, 20);

  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 900">
      <defs>
        <linearGradient id="g" x2="0.9" y2="1">
          <stop stop-color="${palette[0]}"/>
          <stop offset="1" stop-color="#080d18"/>
        </linearGradient>

        <radialGradient id="r">
          <stop stop-color="${palette[1]}" stop-opacity=".85"/>
          <stop offset="1" stop-color="${palette[1]}" stop-opacity="0"/>
        </radialGradient>
      </defs>

      <rect width="600" height="900" fill="url(#g)"/>
      <circle cx="300" cy="450" r="320" fill="url(#r)"/>

      <text
        x="300"
        y="300"
        fill="#ffffff"
        fill-opacity="0.85"
        font-family="Arial,sans-serif"
        font-size="20"
        letter-spacing="4"
        text-anchor="middle">
        ${genre}
      </text>

      <text
        x="300"
        y="460"
        fill="#fff"
        font-family="Georgia,serif"
        font-weight="bold"
        font-size="42"
        text-anchor="middle">
        ${title}
      </text>

      <text
        x="300"
        y="510"
        fill="#d9e2ed"
        font-family="Arial,sans-serif"
        font-size="18"
        text-anchor="middle">
        ${movie.year || ''} · MOVIEMATE
      </text>
    </svg>
  `;

  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}

function posterUrl(movie) {
  return movie.poster_url || movie.poster || posterFallback(movie);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, character => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  })[character]);
}

function posterMarkup(movie, className = '') {
  const fallback = posterFallback(movie);

  return `
    <img
      class="${className}"
      src="${posterUrl(movie)}"
      alt="${escapeHtml(movie.title)} poster"
      loading="lazy"
      onerror="this.onerror=null;this.src='${fallback}'"
    >
  `;
}

function normalizeMovie(movie) {
  const genres = Array.isArray(movie.genres)
    ? movie.genres
    : String(movie.genres || movie.genre || 'General')
        .split('|')
        .filter(Boolean);

  return {
    ...movie,
    id: Number(movie.id),
    genre: movie.genre || genres[0] || 'General',
    genres,
    cast: Array.isArray(movie.cast)
      ? movie.cast
      : String(movie.cast || '')
          .split('|')
          .filter(Boolean),

    keywords: Array.isArray(movie.keywords)
      ? movie.keywords
      : String(movie.keywords || '')
          .split('|')
          .filter(Boolean),

    poster:
      movie.poster_url ||
      movie.poster ||
      posterFallback(movie),

    rating: Number(movie.rating || 0)
  };
}

function syncSearchInputs(value) {
  state.query = value;

  if (filterInput) {
    filterInput.value = value;
  }

  if (filterInputSecondary) {
    filterInputSecondary.value = value;
  }

  renderFilters();
  renderRecommended();

  const trimmed = value.trim();

  if (trimmed.length > 1) {
    const matches = getFilteredMovies();

    if (matches.length >= 1) {
      const topMatchId = normalizeMovie(matches[0]).id;

      const card = document.querySelector(
        `.movie-card[data-id="${topMatchId}"]`
      );

      if (card) {
        card.scrollIntoView({
          behavior: 'smooth',
          block: 'center'
        });

        card.style.outline = '3px solid #e50914';

        setTimeout(() => {
          card.style.outline = '';
        }, 1400);
      }
    }
  }
}

function renderGenres() {
  const allGenres = movies.flatMap(movie => normalizeMovie(movie).genres);

  const uniqueGenres = [
    ...new Set(allGenres)
  ].sort((a, b) => a.localeCompare(b));

  const genres = ['All', ...uniqueGenres];

  if (genreFilter) {
    genreFilter.innerHTML = genres
      .map(genre => `
        <option value="${genre}">
          ${genre}
        </option>
      `)
      .join('');
  }

  const uniqueYears = [
    ...new Set(
      movies.map(movie => Number(normalizeMovie(movie).year))
    )
  ].sort((a, b) => b - a);

  const years = ['All', ...uniqueYears.map(String)];

  if (yearFilter) {
    yearFilter.innerHTML = years
      .map(year => `
        <option value="${year}">
          ${year === 'All' ? 'All years' : year}
        </option>
      `)
      .join('');
  }

  const ratings = ['All', '8+', '9+'];

  if (ratingFilter) {
    ratingFilter.innerHTML = ratings
      .map(level => `
        <option value="${level}">
          ${level === 'All' ? 'Any rating' : level}
        </option>
      `)
      .join('');
  }
}

function getFilteredMovies() {
  const query = state.query.trim().toLowerCase();

  return movies.filter(movie => {
    const item = normalizeMovie(movie);

    const searchText = [
      item.title,
      item.genre,
      item.director,
      item.description,
      ...item.cast
    ]
      .join(' ')
      .toLowerCase();

    const matchesQuery =
      !query || searchText.includes(query);

    const matchesGenre =
      state.genre === 'All' ||
      item.genres.includes(state.genre);

    const matchesYear =
      state.year === 'All' ||
      String(item.year) === state.year;

    const matchesRating =
      state.rating === 'All' ||
      (state.rating === '8+' && item.rating >= 8) ||
      (state.rating === '9+' && item.rating >= 9);

    return (
      matchesQuery &&
      matchesGenre &&
      matchesYear &&
      matchesRating
    );
  });
}

function buildMovieCard(movie) {
  const item = normalizeMovie(movie);
  const isFavorite = state.favorites.has(item.id);
  const genre = item.genres[0] || 'General';

  return `
    <article class="movie-card" data-id="${item.id}">
      <div class="movie-poster">
        ${posterMarkup(item)}

        <div class="movie-overlay"></div>

        <div class="movie-rating">
          ★ ${item.rating.toFixed(1)}
        </div>

        <div class="movie-hover-actions">
          <button
            class="movie-play-button"
            data-action="open"
            data-id="${item.id}"
            title="View details">
            ▶
          </button>

          <button
            class="movie-circle-button"
            data-action="favorite"
            data-id="${item.id}"
            title="Add to My List">
            ${isFavorite ? '✓' : '+'}
          </button>
        </div>
      </div>

      <div class="movie-body">
        <div class="movie-title-row">
          <h3>${escapeHtml(item.title)}</h3>
        </div>

        <div class="movie-meta">
          <span class="match-text">
            ${Math.min(99, Math.round(item.rating * 10 + 5))}% Match
          </span>

          <span>${item.year}</span>
          <span>•</span>
          <span>${genre}</span>
        </div>

        <div class="movie-footer">
          <button
            class="watch-btn"
            data-action="open"
            data-id="${item.id}">
            More Info
          </button>

          <button
            class="heart"
            data-action="favorite"
            data-id="${item.id}"
            aria-label="Favorite movie">
            ${isFavorite ? '♥' : '♡'}
          </button>
        </div>
      </div>
    </article>
  `;
}

function renderTrending() {
  if (!trendingList) return;

  const topMovies = [...movies]
    .sort((a, b) => Number(b.rating) - Number(a.rating))
    .slice(0, 10);

  trendingList.innerHTML = topMovies
    .map(buildMovieCard)
    .join('');

  const featured = normalizeMovie(topMovies[0] || movies[0]);

  const featuredPoster =
    document.getElementById('featuredPoster');

  if (featuredPoster) {
    featuredPoster.src = posterUrl(featured);

    featuredPoster.onerror = () => {
      featuredPoster.onerror = null;
      featuredPoster.src = posterFallback(featured);
    };

    featuredPoster.alt = `${featured.title} poster`;
  }

  const featuredTitle =
    document.getElementById('featuredTitle');

  if (featuredTitle) {
    featuredTitle.textContent = featured.title;
  }

  const featureCardTitle =
    document.getElementById('featureCardTitle');

  if (featureCardTitle) {
    featureCardTitle.textContent =
      state.newUser
        ? 'Popular with MovieMate viewers'
        : `Inspired by ${normalizeMovie(state.selectedMovie).title}`;
  }

  const featureCardText =
    document.getElementById('featureCardText');

  if (featureCardText) {
    featureCardText.textContent =
      state.newUser
        ? 'Start with highly rated picks, then save or rate movies to build your personal recommendations.'
        : 'Your saved movies and ratings are shaping the titles recommended for you.';
  }

  const subtitle =
    document.getElementById('featuredPicksSubtitle');

  if (subtitle) {
    subtitle.textContent =
      state.newUser
        ? 'Popular picks to get you started'
        : `Picked for ${state.displayName}`;
  }
}

function renderWelcomeBanner() {
  const banner =
    document.getElementById('newUserBanner');

  if (!banner) return;

  if (state.newUser) {
    banner.innerHTML = `
      <div class="welcome-banner-content">

        <div>
          <div class="eyebrow">
            Welcome to MovieMate
          </div>

          <h3>
            Hello, ${escapeHtml(state.displayName)}
          </h3>

          <p>
            Explore movies, save favourites and rate titles.
            MovieMate will learn from your activity and create
            personalised recommendations.
          </p>
        </div>

        <button
          class="btn btn-primary"
          data-action="browse-popular">
          Browse Movies
        </button>

      </div>
    `;
  } else {
    banner.innerHTML = `
      <div class="welcome-banner-content">

        <div>
          <div class="eyebrow">
            Personalised for you
          </div>

          <h3>
            Your MovieMate recommendations are ready.
          </h3>

          <p>
            Your ratings and favourites are now influencing
            your recommendations.
          </p>
        </div>

      </div>
    `;
  }
}

function renderRecommended() {
  if (!recommendedList) return;

  const baseMovie =
    normalizeMovie(state.selectedMovie || movies[0]);

  const placeholder = [...movies]
    .sort((a, b) => Number(b.rating) - Number(a.rating))
    .slice(0, 10);

  recommendedList.innerHTML = placeholder
    .map(buildMovieCard)
    .join('');

  const recommendationSubtitle =
    document.getElementById('recommendationSubtitle');

  if (recommendationSubtitle) {
    recommendationSubtitle.textContent =
      state.newUser
        ? 'Popular with viewers'
        : `Inspired by ${baseMovie.title}`;
  }

  const requestId =
    ++recommendationRequestId;

  const trimmedQuery =
    state.query.trim();

  clearTimeout(recommendationTimer);

  recommendationTimer = setTimeout(() => {
    const endpoint =
      !trimmedQuery && state.user
        ? '/api/recommend/hybrid'
        : `/api/recommendations?${new URLSearchParams({
            q: trimmedQuery
          })}`;

    fetch(endpoint)
      .then(response => {
        if (!response.ok) {
          throw new Error(
            'Recommendation request failed'
          );
        }

        return response.json();
      })
      .then(result => {
        if (
          requestId !== recommendationRequestId
        ) {
          return;
        }

        const recommendations =
          result.recommendations || [];

        if (recommendations.length) {
          recommendedList.innerHTML =
            recommendations
              .map(buildMovieCard)
              .join('');
        }

        if (recommendationSubtitle) {
          if (result.matched_movie) {
            recommendationSubtitle.textContent =
              `Similar to ${result.matched_movie}`;

          } else if (
            result.algorithm === 'hybrid'
          ) {
            recommendationSubtitle.textContent =
              'Personalised using content and collaborative filtering';

          } else if (
            result.algorithm === 'content'
          ) {
            recommendationSubtitle.textContent =
              'Based on your saved preferences';

          } else {
            recommendationSubtitle.textContent =
              state.newUser
                ? 'Popular with viewers'
                : 'Recommended for you';
          }
        }
      })
      .catch(error => {
        console.error(
          'Could not load recommendations.',
          error
        );
      });

  }, 250);
}

function renderCollaborative() {
  const section =
    document.getElementById('collaborativeSection');

  const list =
    document.getElementById('collaborativeList');

  if (!section || !list) return;

  fetch('/api/recommend/collaborative')
    .then(response => response.json())
    .then(result => {
      const recommendations =
        result.recommendations || [];

      if (recommendations.length > 0) {
        list.innerHTML =
          recommendations
            .slice(0, 10)
            .map(buildMovieCard)
            .join('');

        section.hidden = false;
      } else {
        section.hidden = true;
        list.innerHTML = '';
      }
    })
    .catch(error => {
      console.error(
        'Could not load collaborative recommendations.',
        error
      );

      section.hidden = true;
    });
}

function renderFilters() {
  const visible = getFilteredMovies();

  const container = document.getElementById('movieList');
  const resultCount = document.getElementById('resultCount');
  const filterMessage = document.getElementById('filterMessage');

  if (!container) return;

  // Show the filtered movies
  container.innerHTML = visible
    .map(buildMovieCard)
    .join('');

  // If no movies match
  if (!visible.length) {
    container.innerHTML = `
      <div class="empty-state">
        <h3>No titles found</h3>
        <p>Try changing your search or filters.</p>
      </div>
    `;
  }

  // Update result count
  if (resultCount) {
    resultCount.textContent =
      `${visible.length} ${visible.length === 1 ? 'title' : 'titles'}`;
  }

  // Build a visible description of active filters
  const activeFilters = [];

  if (state.query.trim()) {
    activeFilters.push(`Search: "${state.query.trim()}"`);
  }

  if (state.genre !== 'All') {
    activeFilters.push(`Genre: ${state.genre}`);
  }

  if (state.year !== 'All') {
    activeFilters.push(`Year: ${state.year}`);
  }

  if (state.rating !== 'All') {
    activeFilters.push(`Rating: ${state.rating}`);
  }

  if (filterMessage) {
    if (activeFilters.length > 0) {
      filterMessage.textContent =
        activeFilters.join(' • ');
    } else {
      filterMessage.textContent =
        'Showing all movies';
    }
  }

  // Keep both search boxes synchronized
  if (
    filterInput &&
    filterInput.value !== state.query
  ) {
    filterInput.value = state.query;
  }

  if (
    filterInputSecondary &&
    filterInputSecondary.value !== state.query
  ) {
    filterInputSecondary.value = state.query;
  }
}

async function openMovieModal(movieId) {
  const selected =
    normalizeMovie(
      movies.find(
        movie =>
          normalizeMovie(movie).id === movieId
      ) || movies[0]
    );

  state.selectedMovie = selected;

  let relatedItems = [];

  try {
    const response =
      await fetch(
        `/api/recommend?movie_id=${selected.id}`
      );

    if (response.ok) {
      const recommendations =
        await response.json();

      if (
        Array.isArray(recommendations) &&
        recommendations.length
      ) {
        relatedItems = recommendations;
      }
    }
  } catch (error) {
    console.error(
      'Could not load recommendations from the model.',
      error
    );
  }

  const generated =
    relatedItems.slice(0, 6);

  modalDetails.innerHTML = `
    <div class="modal-hero">

      <div class="modal-poster">
        ${posterMarkup(selected)}
      </div>

      <div class="modal-body">

        <div class="modal-header">

          <div>
            <div class="modal-match">
              ${Math.min(
                99,
                Math.round(selected.rating * 10 + 5)
              )}% Match
            </div>

            <h3>
              ${escapeHtml(selected.title)}
            </h3>

            <div class="meta-line">
              <span>
                ⭐ ${selected.rating.toFixed(1)}
              </span>

              <span>•</span>

              <span>
                ${selected.year}
              </span>

              <span>•</span>

              <span>
                ${selected.genre}
              </span>
            </div>
          </div>

          <button
            class="close-btn"
            id="closeModal"
            aria-label="Close movie details">
            ✕
          </button>

        </div>

        <p class="modal-description">
          ${escapeHtml(selected.description)}
        </p>

        <div class="movie-details-list">

          <p>
            <strong>Director:</strong>
            ${escapeHtml(selected.director || 'Unknown')}
          </p>

          <p>
            <strong>Cast:</strong>
            ${escapeHtml(
              selected.cast.join(', ') || 'Unknown'
            )}
          </p>

          <p>
            <strong>Genres:</strong>
            ${escapeHtml(
              selected.genres.join(', ')
            )}
          </p>

        </div>

        <div class="action-row">

          <button
            class="btn btn-primary"
            data-action="rate"
            data-id="${selected.id}">
            ⭐ Rate
          </button>

          <button
            class="btn btn-secondary"
            data-action="favorite"
            data-id="${selected.id}">
            ${
              state.favorites.has(selected.id)
                ? '✓ In My List'
                : '+ My List'
            }
          </button>

        </div>

      </div>

    </div>
  `;

  if (generated.length) {
    const relatedList =
      generated
        .map(buildMovieCard)
        .join('');

    modalDetails.insertAdjacentHTML(
      'beforeend',
      `
        <section class="section modal-recommendations">

          <div class="section-header">

            <div>
              <p class="section-kicker">
                Recommended
              </p>

              <h2>
                More like
                ${escapeHtml(selected.title)}
              </h2>
            </div>

          </div>

          <div class="movie-row">
            ${relatedList}
          </div>

        </section>
      `
    );
  }

  if (modal) {
    modal.classList.add('open');
  }

  document.body.classList.add(
    'modal-locked'
  );

  const closeButton =
    document.getElementById('closeModal');

  if (closeButton) {
    closeButton.addEventListener(
      'click',
      closeModal
    );
  }
}

function closeModal() {
  if (modal) {
    modal.classList.remove('open');
  }

  document.body.classList.remove(
    'modal-locked'
  );

  if (modalDetails) {
    modalDetails.innerHTML = '';
  }
}

function openTopSearchMatch() {
  const matches =
    getFilteredMovies();

  if (matches.length > 0) {
    const topMatchId =
      normalizeMovie(matches[0]).id;

    openMovieModal(topMatchId);
  }
}

function setAuthMode(mode) {
  authMode = mode;

  const registering =
    mode === 'register';

  const authTitle =
    document.getElementById('authTitle');

  const authIntro =
    document.getElementById('authIntro');

  const nameField =
    document.getElementById('nameField');

  const submit =
    document.getElementById('authSubmit');

  const authSwitch =
    document.getElementById('authSwitch');

  const authError =
    document.getElementById('authError');

  if (authTitle) {
    authTitle.textContent =
      registering
        ? 'Create your account'
        : 'Welcome back';
  }

  if (authIntro) {
    authIntro.textContent =
      registering
        ? 'Create your profile and start receiving personalised recommendations.'
        : 'Sign in to continue your MovieMate experience.';
  }

  if (nameField) {
    nameField.hidden = !registering;
  }

  if (authForm?.elements?.name) {
    authForm.elements.name.required =
      registering;
  }

  if (authForm?.elements?.password) {
    authForm.elements.password.autocomplete =
      registering
        ? 'new-password'
        : 'current-password';
  }

  if (submit) {
    submit.textContent =
      registering
        ? 'Create account'
        : 'Sign in';
  }

  if (authSwitch) {
    authSwitch.textContent =
      registering
        ? 'Already have an account? Sign in'
        : 'New to MovieMate? Create an account';
  }

  if (authError) {
    authError.textContent = '';
  }
}

function openAuth(mode) {
  setAuthMode(mode);

  if (authModal) {
    authModal.classList.add('open');
  }

  if (authForm?.elements?.email) {
    authForm.elements.email.focus();
  }
}

async function persistActivity() {
  if (!state.user) return;

  try {
    await fetch('/api/profile', {
      method: 'PUT',

      headers: {
        'Content-Type': 'application/json'
      },

      body: JSON.stringify({
        favorites: [
          ...state.favorites
        ],

        ratings:
          state.userRatings
      })
    });
  } catch (error) {
    console.error(
      'Could not save profile activity.',
      error
    );
  }
}

function applyAccount(payload) {
  state.user =
    payload.user;

  state.displayName =
    payload.user.name;

  state.favorites =
    new Set(payload.favorites || []);

  state.userRatings =
    payload.ratings || {};

  state.newUser =
    state.favorites.size === 0 &&
    Object.keys(
      state.userRatings
    ).length === 0;

  if (authModal) {
    authModal.classList.remove('open');
  }

  renderWelcomeBanner();
  renderTrending();
  renderRecommended();
  renderCollaborative();
  renderFilters();
  renderMyList();
  renderProfile();

  const accountButton =
    document.querySelector(
      '[data-action="auth-open"][data-mode="login"]'
    );

  if (accountButton) {
    const label =
      accountButton.querySelector(
        '.profile-label'
      );

    if (label) {
      label.textContent =
        state.displayName;
    } else {
      accountButton.textContent =
        state.displayName;
    }

    accountButton.dataset.action =
      'auth-logout';
  }
}

function toggleFavorite(movieId) {
  if (
    state.favorites.has(movieId)
  ) {
    state.favorites.delete(movieId);
  } else {
    state.favorites.add(movieId);
    state.newUser = false;
  }

  renderWelcomeBanner();
  renderTrending();
  renderRecommended();
  renderCollaborative();
  renderFilters();
  renderMyList();
  renderProfile();

  persistActivity();
}

function attachHandlers() {

  if (filterInput) {
    filterInput.addEventListener(
      'input',
      event => {
        syncSearchInputs(
          event.target.value
        );
      }
    );

    filterInput.addEventListener(
      'keydown',
      event => {
        if (event.key === 'Enter') {
          event.preventDefault();

          renderFilters();

          const library = document.getElementById('movieList');

          if (library) {
            library.scrollIntoView({
              behavior: 'smooth',
              block: 'start'
            });
          }
        }
      }
    );
  }

  if (filterInputSecondary) {
    filterInputSecondary.addEventListener(
      'input',
      event => {
        syncSearchInputs(
          event.target.value
        );
      }
    );

    filterInputSecondary.addEventListener(
      'keydown',
      event => {
        if (event.key === 'Enter') {
          event.preventDefault();
          openTopSearchMatch();
        }
      }
    );
  }

    if (genreFilter) {
      genreFilter.addEventListener(
        'change',
        event => {
          state.genre = event.target.value;

          renderFilters();

          document
            .getElementById('movieList')
            ?.scrollIntoView({
              behavior: 'smooth',
              block: 'start'
            });
        }
      );
    }

    if (yearFilter) {
      yearFilter.addEventListener(
        'change',
        event => {
          state.year = event.target.value;

          renderFilters();

          document
            .getElementById('movieList')
            ?.scrollIntoView({
              behavior: 'smooth',
              block: 'start'
            });
        }
      );
    }

    if (ratingFilter) {
      ratingFilter.addEventListener(
        'change',
        event => {
          state.rating = event.target.value;

          renderFilters();

          document
            .getElementById('movieList')
            ?.scrollIntoView({
              behavior: 'smooth',
              block: 'start'
            });
        }
      );
    }

  document.addEventListener(
    'click',
    event => {
      const actionTarget =
        event.target.closest(
          '[data-action]'
        );

      if (!actionTarget) return;

      const action =
        actionTarget.dataset.action;

      if (action === 'auth-open') {
        openAuth(
          actionTarget.dataset.mode
        );

        return;
      }

      if (action === 'auth-close') {
        if (authModal) {
          authModal.classList.remove(
            'open'
          );
        }

        return;
      }

      if (action === 'auth-logout') {
        fetch(
          '/api/auth/logout',
          {
            method: 'POST'
          }
        );

        state.user = null;
        state.favorites.clear();
        state.userRatings = {};
        state.newUser = true;
        state.displayName =
          'New User';

        const label =
          actionTarget.querySelector(
            '.profile-label'
          );

        if (label) {
          label.textContent =
            'Sign in';
        } else {
          actionTarget.textContent =
            'Sign in';
        }

        actionTarget.dataset.action =
          'auth-open';

        actionTarget.dataset.mode =
          'login';

        renderWelcomeBanner();
        renderTrending();
        renderRecommended();
        renderCollaborative();
        renderFilters();
        renderMyList();
        renderProfile();

        return;
      }

      const movieId =
        Number(
          actionTarget.dataset.id
        );

      if (action === 'open') {
        openMovieModal(movieId);
      }

      if (action === 'favorite') {
        toggleFavorite(movieId);
      }

      if (
        action === 'browse-popular'
      ) {
        const section =
          document.getElementById(
            'trendingList'
          );

        if (section) {
          section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }

      if (action === 'rate') {
        const movie =
          movies.find(
            item =>
              normalizeMovie(item).id ===
              movieId
          );

        if (movie) {
          const item =
            normalizeMovie(movie);

          const currentRating =
            state.userRatings[
              item.id
            ] || '4';

          const newRating =
            Number(
              prompt(
                `Rate ${item.title} from 1 to 5`,
                currentRating
              )
            );

          if (
            !Number.isNaN(newRating) &&
            newRating >= 1 &&
            newRating <= 5
          ) {
            state.userRatings[
              item.id
            ] = newRating;

            state.newUser = false;

            renderWelcomeBanner();
            renderProfile();
            renderRecommended();
            renderCollaborative();

            persistActivity();

            alert(
              `You rated ${item.title} ${newRating}/5.`
            );
          }
        }
      }
    }
  );

  if (modal) {
    modal.addEventListener(
      'click',
      event => {
        if (
          event.target === modal
        ) {
          closeModal();
        }
      }
    );
  }

  if (authModal) {
    authModal.addEventListener(
      'click',
      event => {
        if (
          event.target === authModal
        ) {
          authModal.classList.remove(
            'open'
          );
        }
      }
    );
  }

  const authSwitch =
    document.getElementById(
      'authSwitch'
    );

  if (authSwitch) {
    authSwitch.addEventListener(
      'click',
      () => {
        setAuthMode(
          authMode === 'login'
            ? 'register'
            : 'login'
        );
      }
    );
  }

  if (authForm) {
    authForm.addEventListener(
      'submit',
      async event => {
        event.preventDefault();

        const formData =
          new FormData(authForm);

        const payload =
          Object.fromEntries(
            formData.entries()
          );

        const endpoint =
          authMode === 'register'
            ? '/api/auth/register'
            : '/api/auth/login';

        const submit =
          document.getElementById(
            'authSubmit'
          );

        if (submit) {
          submit.disabled = true;
          submit.textContent =
            'Please wait...';
        }

        try {
          const response =
            await fetch(
              endpoint,
              {
                method: 'POST',

                headers: {
                  'Content-Type':
                    'application/json'
                },

                body:
                  JSON.stringify(payload)
              }
            );

          const result =
            await response.json();

          if (!response.ok) {
            throw new Error(
              result.error ||
              'Could not complete sign in.'
            );
          }

          applyAccount(result);

        } catch (error) {

          const authError =
            document.getElementById(
              'authError'
            );

          if (authError) {
            authError.textContent =
              error.message;
          }

        } finally {

          if (submit) {
            submit.disabled = false;

            submit.textContent =
              authMode === 'register'
                ? 'Create account'
                : 'Sign in';
          }
        }
      }
    );
  }
}

function renderMyList() {
  const container = document.getElementById('myListMovies');
  const section = document.getElementById('myListSection');

  if (!container || !section) return;

  const savedMovies = movies.filter(movie =>
    state.favorites.has(normalizeMovie(movie).id)
  );

  if (savedMovies.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <h3>Your list is empty</h3>
        <p>
          Click the heart or + button on a movie to save it here.
        </p>
      </div>
    `;

    return;
  }

  container.innerHTML = savedMovies
    .map(buildMovieCard)
    .join('');
}

function renderProfile() {
  const favoriteMovies =
    movies.filter(movie =>
      state.favorites.has(
        normalizeMovie(movie).id
      )
    );

  const genreCounts = {};

  favoriteMovies.forEach(movie => {
    normalizeMovie(movie)
      .genres
      .forEach(genre => {
        genreCounts[genre] =
          (genreCounts[genre] || 0) + 1;
      });
  });

  let userGenreTags =
    Object.entries(genreCounts)
      .sort(
        (a, b) =>
          b[1] - a[1]
      )
      .slice(0, 5)
      .map(([genre]) => genre);

  if (!userGenreTags.length) {
    userGenreTags = [
      'Action',
      'Sci-Fi',
      'Drama'
    ];
  }

  const ratingList =
    Object.entries(
      state.userRatings
    )
      .map(
        ([id, score]) => {
          const movie =
            movies.find(
              item =>
                normalizeMovie(item).id ===
                Number(id)
            );

          if (!movie) return '';

          const item =
            normalizeMovie(movie);

          return `
            <div class="rating-item">

              <span>
                ${escapeHtml(item.title)}
              </span>

              <span class="rating-stars">
                ${'★'.repeat(score)}
                ${'☆'.repeat(5 - score)}
              </span>

            </div>
          `;
        }
      )
      .join('');

  const favoriteCount =
    document.getElementById(
      'favoriteMovies'
    );

  if (favoriteCount) {
    favoriteCount.textContent =
      favoriteMovies.length;
  }

  const genreTags =
    document.getElementById(
      'genreTags'
    );

  if (genreTags) {
    genreTags.innerHTML =
      userGenreTags
        .map(
          tag => `
            <span class="tag">
              ${tag}
            </span>
          `
        )
        .join('');
  }

  const ratingContainer =
    document.getElementById(
      'ratingList'
    );

  if (ratingContainer) {
    ratingContainer.innerHTML =
      ratingList ||
      `
        <div class="rating-item">
          <span>
            No ratings yet.
            Rate a movie to improve
            your recommendations.
          </span>
        </div>
      `;
  }
}

async function loadMovies() {
  try {
    const response =
      await fetch('/api/movies');

    if (!response.ok) {
      throw new Error(
        'API request failed'
      );
    }

    const data =
      await response.json();

    if (
      Array.isArray(data) &&
      data.length
    ) {
      movies =
        data.map(normalizeMovie);

      state.selectedMovie =
        movies[0];
    }

  } catch (error) {

    console.error(
      'Could not load movies from Flask. Using fallback movies.',
      error
    );

    movies =
      fallbackMovies.map(
        normalizeMovie
      );

    state.selectedMovie =
      movies[0];
  }

  try {
    const response =
      await fetch('/api/profile');

    if (response.ok) {
      const profile =
        await response.json();

      if (profile.user) {
        applyAccount(profile);
      }
    }

  } catch (error) {

    console.error(
      'Could not restore account session.',
      error
    );
  }

  renderGenres();
  renderWelcomeBanner();
  renderTrending();
  renderRecommended();
  renderCollaborative();
  renderFilters();
  renderMyList();
  renderProfile();
}

function init() {
  attachHandlers();
  loadMovies();
}

init();