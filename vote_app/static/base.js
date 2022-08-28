
charts = {};
function fetch_data(element, first) {
    fetch(element.dataset.url).then(e => e.json()).then(received_data => {
        console.log(received_data);
        construct_chart(element, received_data, first)

    })

}
function construct_chart(element, received_data, first) {
    if (first == true) {
        let config = {
            type: 'bar',
            data: {
                datasets: [{
                    data: received_data['values'],
                    borderColor: "#444",
                    backgroundColor: ["blue", 'gold', 'cyan', 'purple'],
                    colors: ["red", "blue", "cyan", "green"],
                    borderWidth: 4,
                    fill: false,
                    label: element.dataset.title
                }],
                labels: received_data['labels']
            },
            options: {
                responsive: true
            }
        };
        let chart = new Chart(
            element, config
        )
        charts[element.id] = { chart: chart, config: config }
    } else {
        chart_group = charts[element.id];
        chart = chart_group.chart;
        config = chart_group.config;
        config.data.labels = received_data['labels'];
        config.data.datasets[0].data = received_data['values'];
        chart.update()
    }
    document.getElementById(`total-votes-${element.dataset.id}`).innerText = received_data['total_votes']
    
    if (element.dataset.ended == "false") {
        setTimeout(fetch_data, 7000, element, false)
    }

}

function setup() {
    addAnimationObserver();
    let elements = document.querySelectorAll('.election_canvas');
    for (element of elements) {
        fetch_data(element, first = true);
    }
}
function addAnimationObserver() {

    const observer = new IntersectionObserver(entries => {
        // Loop over the entries
        entries.forEach(entry => {
            // If the element is visible
            if (entry.isIntersecting) {
                // Add the animation class
                entry.target.classList.add('animate__animated');
            }
        });
    });
    for (element of document.querySelectorAll('.animate')) {

        observer.observe(element);
    }

}


window.onload = setup

