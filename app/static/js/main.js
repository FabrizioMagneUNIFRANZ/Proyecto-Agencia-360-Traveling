document.addEventListener('DOMContentLoaded', () => {
    // Tab switching logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const searchBtnText = document.getElementById('search-btn-text');
    let currentTab = 'vuelos';
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            currentTab = btn.getAttribute('data-tab');
            updateFormLayout(currentTab);
        });
    });

    // Check for hash on load
    const hash = window.location.hash.substring(1);
    if (['vuelos', 'hoteles', 'vuelo_hotel', 'transporte', 'seguros', 'actividades'].includes(hash)) {
        const targetBtn = document.querySelector(`.tab-btn[data-tab="${hash}"]`);
        if (targetBtn) targetBtn.click();
    }

    function updateFormLayout(tab) {
        const destGroup = document.getElementById('destination-group');
        const returnGroup = document.getElementById('return-group');
        const swapBtn = document.getElementById('swap-locations');
        const originLabel = document.querySelector('label[for="origin"]');
        const originInput = document.getElementById('origin');
        const depLabel = document.getElementById('departure-label');
        const tripTypeSelector = document.getElementById('trip-type-selector');

        if (!originLabel) return; // Not on home page

        if (tab === 'hoteles') {
            originLabel.innerHTML = '<i class="fa-solid fa-location-dot"></i> Destino o Hotel';
            originInput.placeholder = '¿A dónde viajas?';
            destGroup.style.display = 'none';
            swapBtn.style.display = 'none';
            returnGroup.style.display = 'block';
            depLabel.innerHTML = '<i class="fa-regular fa-calendar"></i> Entrada';
            document.getElementById('return-label').innerHTML = '<i class="fa-regular fa-calendar"></i> Salida';
            searchBtnText.textContent = 'Buscar Hoteles';
            tripTypeSelector.style.visibility = 'hidden';
            document.getElementById('form-grid').className = 'form-grid hotels-grid';
        } else if (tab === 'transporte') {
            originLabel.innerHTML = '<i class="fa-solid fa-location-dot"></i> Ciudad o Aeropuerto';
            originInput.placeholder = '¿Dónde necesitas transporte?';
            destGroup.style.display = 'none';
            swapBtn.style.display = 'none';
            returnGroup.style.display = 'none';
            depLabel.innerHTML = '<i class="fa-regular fa-calendar"></i> Fecha';
            searchBtnText.textContent = 'Buscar Transporte';
            tripTypeSelector.style.visibility = 'hidden';
            document.getElementById('form-grid').className = 'form-grid hotels-grid';
        } else if (tab === 'seguros') {
            originLabel.innerHTML = '<i class="fa-solid fa-shield-halved"></i> Tipo de Viaje';
            originInput.placeholder = 'Ej. Internacional o Nacional';
            destGroup.style.display = 'none';
            swapBtn.style.display = 'none';
            returnGroup.style.display = 'none';
            depLabel.innerHTML = '<i class="fa-regular fa-calendar"></i> Fecha de Inicio';
            searchBtnText.textContent = 'Buscar Seguros';
            tripTypeSelector.style.visibility = 'hidden';
            document.getElementById('form-grid').className = 'form-grid hotels-grid';
        } else if (tab === 'actividades') {
            originLabel.innerHTML = '<i class="fa-solid fa-location-dot"></i> Destino';
            originInput.placeholder = '¿Qué ciudad quieres explorar?';
            destGroup.style.display = 'none';
            swapBtn.style.display = 'none';
            returnGroup.style.display = 'none';
            depLabel.innerHTML = '<i class="fa-regular fa-calendar"></i> Fecha';
            searchBtnText.textContent = 'Buscar Actividades';
            tripTypeSelector.style.visibility = 'hidden';
            document.getElementById('form-grid').className = 'form-grid hotels-grid';
        } else if (tab === 'vuelo_hotel') {
            originLabel.innerHTML = '<i class="fa-solid fa-location-dot"></i> Origen';
            originInput.placeholder = 'Ej. Santa Cruz (VVI)';
            destGroup.style.display = 'block';
            document.querySelector('label[for="destination"]').innerHTML = '<i class="fa-solid fa-location-dot"></i> Destino / Hotel';
            swapBtn.style.display = 'flex';
            returnGroup.style.display = 'block';
            depLabel.innerHTML = '<i class="fa-regular fa-calendar"></i> Salida';
            document.getElementById('return-label').innerHTML = '<i class="fa-regular fa-calendar"></i> Regreso';
            searchBtnText.textContent = 'Buscar Vuelo + Hotel';
            tripTypeSelector.style.visibility = 'visible';
            document.getElementById('form-grid').className = 'form-grid flights-grid';
        } else {
            originLabel.innerHTML = '<i class="fa-solid fa-location-dot"></i> Origen';
            originInput.placeholder = 'Ej. Santa Cruz (VVI)';
            destGroup.style.display = 'block';
            document.querySelector('label[for="destination"]').innerHTML = '<i class="fa-solid fa-location-dot"></i> Destino';
            swapBtn.style.display = 'flex';
            returnGroup.style.display = 'block';
            depLabel.innerHTML = '<i class="fa-regular fa-calendar"></i> Ida';
            document.getElementById('return-label').innerHTML = '<i class="fa-regular fa-calendar"></i> Vuelta';
            searchBtnText.textContent = 'Buscar Vuelos';
            tripTypeSelector.style.visibility = 'visible';
            document.getElementById('form-grid').className = 'form-grid flights-grid';
        }
    }

    // Swap locations logic
    const swapBtn = document.getElementById('swap-locations');
    if (swapBtn) {
        swapBtn.addEventListener('click', () => {
            const origin = document.getElementById('origin');
            const destination = document.getElementById('destination');
            const temp = origin.value;
            origin.value = destination.value;
            destination.value = temp;
            
            swapBtn.style.transform = 'rotate(180deg)';
            setTimeout(() => { swapBtn.style.transform = 'rotate(0deg)'; }, 300);
        });
    }

    // Search functionality - Redirect to Results page
    const mainSearchBtn = document.getElementById('main-search-btn');
    if (mainSearchBtn) {
        mainSearchBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const origin = document.getElementById('origin').value;
            const destination = document.getElementById('destination').value;
            const departure = document.getElementById('departure').value;
            
            if (currentTab === 'vuelos' && (!origin || !destination)) {
                alert('Por favor complete origen y destino');
                return;
            }
            if (currentTab === 'hoteles' && !origin) {
                alert('Por favor ingrese un destino');
                return;
            }
            if (currentTab === 'transporte' && !origin) {
                alert('Por favor ingrese una ciudad');
                return;
            }
            if (currentTab === 'actividades' && !origin) {
                alert('Por favor ingrese un destino para las actividades');
                return;
            }
            if (currentTab === 'seguros' && !departure) {
                alert('Por favor ingrese la fecha de inicio del seguro');
                return;
            }

            // Redirect to results page with parameters
            const searchContext = {
                origen: origin,
                destino: destination,
                fecha: departure,
                regreso: document.getElementById('return') ? document.getElementById('return').value : '',
                adultos: passengers.adults,
                niños: passengers.children,
                pasajeros: passengers.adults + passengers.children
            };
            localStorage.setItem('search_context', JSON.stringify(searchContext));

            let url = `/results?type=${currentTab}&origen=${encodeURIComponent(origin)}&destino=${encodeURIComponent(destination)}&fecha=${departure}`;
            window.location.href = url;
        });
    }

    // Simple scroll effect for navbar
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (navbar && window.scrollY > 20) {
            navbar.style.padding = '5px 0';
        } else if (navbar) {
            navbar.style.padding = '15px 0';
        }
    });

    // Passenger Selector Logic
    const passengerDisplay = document.getElementById('passenger-display-btn');
    const passengerDropdown = document.getElementById('passenger-dropdown');
    const closePassengers = document.getElementById('close-passengers');
    const countBtns = document.querySelectorAll('.count-btn');
    
    let passengers = {
        adults: 1,
        children: 0
    };

    if (passengerDisplay) {
        passengerDisplay.addEventListener('click', (e) => {
            e.stopPropagation();
            passengerDropdown.classList.toggle('active');
        });

        closePassengers.addEventListener('click', () => {
            passengerDropdown.classList.remove('active');
        });

        document.addEventListener('click', (e) => {
            if (!passengerDropdown.contains(e.target) && e.target !== passengerDisplay) {
                passengerDropdown.classList.remove('active');
            }
        });

        countBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const type = btn.getAttribute('data-type');
                const action = btn.getAttribute('data-action');
                const total = passengers.adults + passengers.children;

                if (action === 'add') {
                    if (total < 9) {
                        passengers[type]++;
                    } else {
                        alert('Máximo 9 personas en total');
                    }
                } else {
                    if (type === 'adults' && passengers.adults > 1) {
                        passengers.adults--;
                    } else if (type === 'children' && passengers.children > 0) {
                        passengers.children--;
                    }
                }

                updatePassengerDisplay();
            });
        });
    }

    function updatePassengerDisplay() {
        document.getElementById('count-adults').textContent = passengers.adults;
        document.getElementById('count-children').textContent = passengers.children;
        
        const total = passengers.adults + passengers.children;
        passengerDisplay.textContent = `${passengers.adults} Adulto${passengers.adults > 1 ? 's' : ''}, ${passengers.children} Niño${passengers.children !== 1 ? 's' : ''}`;
        
        // Update context if it exists
        const context = JSON.parse(localStorage.getItem('search_context')) || {};
        context.adultos = passengers.adults;
        context.niños = passengers.children;
        context.pasajeros = total;
        localStorage.setItem('search_context', JSON.stringify(context));
    }
});