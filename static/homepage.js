  "use strict";
  let submitButton = document.querySelector("#sights");

  function showDetails(result) {
    console.log(result)
    // show message to user it was added

  }

  function addSight(param) {
    if (param.innerText === "Add sight to trip") {
      param.innerText = "Sight added";
    }
    let sight = document.querySelector(`a#${param.id}`);
    console.log(sight.innerText); //getting sight

    let trip = $(`select#${param.id}`).find(':selected').text();
    console.log(trip.trim()); //getting trip selected

    let formInputs = {'city': $("#city").val(),
                    'sight_name': sight.innerText,
                    'trip': trip.trim(),
                    'category':$("#categories").val()
                     }

    $.post("/add-sights", formInputs, showDetails);
  }

  // once click, function that adds to details page

  function showResults(result) {
    console.log(result)

    let topSights = result[0]
    let cityCenterLatLong = result[1]
    let sightCoordinates = result[2]
    let imageUrl = result[3]
    let sightURL = result[4]
    let trips = result[5]
    
    
    for (let i = 0; i < topSights.length; i++){
        $('#list_items').append(`<li><img src=${imageUrl[i]} style="width:100px;height:100px"> <br> 
        <a id=addSight_${i} href=${sightURL[i]} target="_blank">${topSights[i]}</a></li>`)

            let session = document.querySelector('#is_session');
            if (session.value === "true") {

              let trip_strings = []

                for (let j = 0; j < trips.length; j++) {
                    trip_strings.push(`<option id=addSight_${j} class=addSight_${j} value=addSight_${j}> ${trips[j]} </option>`)
                  }
                  
              $('#list_items').append(`<form><select id=addSight_${i} name="add-to-trip")>
                ${trip_strings}
                  </select></form>

                <button id=addSight_${i} class='addSightText' onClick="addSight(this); this.onclick=null; this.diabled= true">Add sight to trip</button><br><br>`)
            }
    }

    let map = new google.maps.Map(document.querySelector('#map'), {
      center: cityCenterLatLong, 
      zoom: 8,
    })
    for (let i = 0; i < sightCoordinates.length; i++){
      let marker = new google.maps.Marker({
        position: new google.maps.LatLng(sightCoordinates[i]["latitude"],sightCoordinates[i]["longitude"]),
        map: map,
      })

      google.maps.event.addListener(marker,'click', function() {
          map.setZoom(14);
          map.setCenter(marker.getPosition());
          });
        

    // Construct a new InfoWindow.
      let infoWindow = new google.maps.InfoWindow({
        content: (`${topSights[i]}`)
      });

      // Opens the InfoWindow when marker is clicked.
      marker.addListener('click', function() {
        infoWindow.open(map, marker);
        });
    }
  }

  function submitCity(evt) {
    evt.preventDefault();
    let formInputs = {'city': $("#city").val(),
                      'categories':$("#categories").val()}
    
    $.get("/city", formInputs, showResults);
  }

  submitButton.addEventListener("submit", submitCity);