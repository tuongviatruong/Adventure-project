 "use strict"
  function confirmDel(results) {
    document.location.reload()
  }

  function deleteSight(param) {
    let delSight = document.querySelector(`p#${param.id}`);
    console.log(delSight.innerText);
    let trip = document.getElementById("trip");
    console.log(trip.innerText);
    var confirmationdel = confirm("Are you sure you want to delete this?")
    if (confirmationdel) {
      let formInputs = {'sight_del': delSight.innerText.trim(),
                        'trip': trip.innerText.trim()}
      $.post("/delete_sight", formInputs, confirmDel);
    }
  }

  function refreshTodo(results) {
    document.location.reload()
  }  

  function showInput() {
    let tripp = document.getElementById("trip");
    console.log(tripp.innerText)
    let todo = document.getElementById("todo").value
    console.log(todo)
    
    let formInputs = {'todo': todo,
                    'tripp': tripp.innerText.trim()}
      $.post("/todo", formInputs, refreshTodo);
    
  }

  function refreshDone(results) {
    document.location.reload()
  } 

  function todoDone(param) {
    let trip = document.getElementById("trip");
    console.log(trip.innerText)

    let done = $("input[type=checkbox]:checked").val()
    console.log(done)

    let formInputs = {'done': done,
                    'trip': trip.innerText.trim()}
    $.post("/delete_done", formInputs, refreshDone);
    
  }

 