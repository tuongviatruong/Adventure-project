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
        $('#list_items').append(`<li><a id=addSight_${i} href=${sightURL[i]} target="_blank">${topSights[i]}</a><br>
                    <img src=${imageUrl[i]} class="sightImage"><br></li>`)

            let session = document.querySelector('#is_session');
            if (session.value === "true") {

              let trip_strings = []

                for (let j = 0; j < trips.length; j++) {
                    trip_strings.push(`<option id=addSight_${j} class=addSight_${j} value=addSight_${j}> ${trips[j]} </option>`)
                  }
                  
              $('#list_items').append(`<form><select id=addSight_${i} name="add-to-trip" class="selectpicker form-control1")>
                ${trip_strings}
                  </select></form>

                <button id=addSight_${i} class="btn btn-info" onClick="addSight(this); this.onclick=null; this.diabled= true">Add sight to trip</button><br><br>`)
            }
    }

    let map = new google.maps.Map(document.querySelector('#map'), {
      center: cityCenterLatLong, 
      zoom: 12,
      styles: [{"featureType":"all","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"administrative","elementType":"all","stylers":[{"visibility":"simplified"},{"color":"#5b6571"},{"lightness":"35"}]},{"featureType":"administrative.neighborhood","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"landscape","elementType":"all","stylers":[{"visibility":"on"},{"color":"#f3f4f4"}]},{"featureType":"landscape.man_made","elementType":"geometry","stylers":[{"weight":0.9},{"visibility":"off"}]},{"featureType":"poi.park","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#83cead"}]},{"featureType":"road","elementType":"all","stylers":[{"visibility":"on"},{"color":"#ffffff"}]},{"featureType":"road","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"on"},{"color":"#fee379"}]},{"featureType":"road.highway","elementType":"geometry","stylers":[{"visibility":"on"}]},{"featureType":"road.highway","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"road.highway","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"road.highway.controlled_access","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"road.arterial","elementType":"all","stylers":[{"visibility":"simplified"},{"color":"#ffffff"}]},{"featureType":"road.arterial","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"all","stylers":[{"visibility":"on"},{"color":"#7fc8ed"}]}]
                      
    })
    for (let i = 0; i < sightCoordinates.length; i++){
      let myImageURL = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAI8SURBVGhD7ZXBS1RRFMYHXIRRupNaOfNmaqG7ysowQQJxEaEw781k04A42SKQEoQKI3DRqBBpbqTViOLGjRtxnc5MzODf0KJFMxK5H6N7OufN4SXjZXT3zsP7gw/uu/eew/e9e+dNyHAegNFrlnKs96hdlbC+s77SHK3xNrmoodgFlYh8Rv2BhAU6KSdyhFqivVwmC/Uk1oYBip7pF30A8xmAldcA2TFdoALYXZe4XA5obMs1+bQLYPkVwObSf619AEhGdWG2uFwGKmmNuOYeXwf4MlM3v7EAMDsK8PIBQBrDNYTw5ESHuY3/4A/5m2vqXbweYn0OIHNLb7xBdB25jb+A3XkFv0Z/XWO52XqQyQGtaZ2oVqWsDm7nH8oJ97umxm/ylZrX/h6aCU/lPrfzD5UMP3INTfTUg6y80ZptJurB7fxDJaL3PFNTg3gyN04YPU3K6bzL7fwDbKud/uR0Bs8ivFY16sHt/AWD7OhMnkUYZJvb+I+KR3vxE6x0RpuJakRcq+Pgm/2kM9tM+On9yOVyADvUgmFWdYb1iuSohsvlgW/5OV6Zit68ewo/lR1+xttlAw+vXqxlbqcr2Wn4/Tbtisa18TspWuNtwWB//7C9UD6A46I5Xg4OJog0TBBpmCDSMEGkYYJIwwSRhgkiDRNEGiaINEwQaZgg0sjnf11uDEJzvBwsCqXqnhcExzwdPPLlaso7DRzzdPAoFn+0FsrVQxKNeTqY5EsHiyR+DC57pUo3iR8N54RQ6B8nz08tnO5GhAAAAABJRU5ErkJggg==';
      let marker = new google.maps.Marker({
        position: new google.maps.LatLng(sightCoordinates[i]["latitude"],sightCoordinates[i]["longitude"]),
        map: map,
        icon: myImageURL
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