console.log('[Start]Terminal works propperly')
var map = L.map('map').setView([43.167787923247005, -2.627729963770382], 12.0);

L.tileLayer('file:///Z%3A/Spain/map/{z}/{x}/{y}.png', {
    maxZoom: 15,
}).addTo(map);

const iconMarker_helicopter = L.icon({
    iconUrl: 'public/images/helicopter-map.png',
    iconSize: [70, 70],
    
})

var url = 'http://127.0.0.1:5000//helicopter_1.json'

let marker_helicopter = null
const updateMap = () => {
    const helicopter_1 = url
    fetch(helicopter_1)
      .then(res => res.json())
      .then(data => {
        if (marker_helicopter) {
          map.removeLayer(marker_helicopter)
        }
        const {
          latitude,
          longitude
        } = data.helicopter1_position
        console.log(latitude, longitude)
        marker_helicopter = L.marker([latitude, longitude], {
          icon: iconMarker_helicopter
        }).addTo(map)
      })
  
    setTimeout(updateMap, 2000)
}

updateMap()
