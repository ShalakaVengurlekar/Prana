//! Active Navbar Item

const navItems = document.querySelectorAll(".nav-item");

navItems.forEach((navItem, i) => {
  navItem.addEventListener("click", () => {
    navItems.forEach((item, j) => {
      item.className = "nav-item";
    });
    navItem.className = "nav-item active";
  });
});

//! Light/Dark Mode

const moonIcon = document.querySelector(".moon");
const sunIcon = document.querySelector(".sun");
const nightImage = document.querySelector(".night-img");
const morningImage = document.querySelector(".morning-img");
const toggle = document.querySelector(".toggle");

function switchTheme() {
  document.body.classList.toggle("darkmode");
  if (document.body.classList.contains("darkmode")) {
    sunIcon.classList.remove("hidden");
    moonIcon.classList.add("hidden");
    morningImage.classList.add("hidden");
    nightImage.classList.remove("hidden");
    localStorage.setItem("theme", "dark");
  } else {
    sunIcon.classList.add("hidden");
    moonIcon.classList.remove("hidden");
    morningImage.classList.remove("hidden");
    nightImage.classList.add("hidden");
    localStorage.setItem("theme", "light");
  }
}

//! Share Button Popup

const sharebtns = document.querySelectorAll(".share-btn");

sharebtns.forEach((btn) => {
  btn.addEventListener("click", (event) => {
    const popup = btn.closest(".event-footer").querySelector(".popup");

    btn.classList.toggle("active");
    popup.classList.toggle("active");

    event.stopPropagation();
  });
});

document.addEventListener("click", (event) => {
  const popups = document.querySelectorAll(".popup");

  popups.forEach((popup) => {
    if (popup.classList.contains("active") && !popup.contains(event.target)) {
      popup.classList.remove("active");

      const shareBtn = popup
        .closest(".event-footer")
        .querySelector(".share-btn");
      shareBtn.classList.remove("active");
    }
  });
});

//! Like Buttons

const likeBtns = document.querySelectorAll(".like-btn");

likeBtns.forEach((likeBtn) => {
  likeBtn.addEventListener("click", () => {
    if (likeBtn.classList.contains("bxs-heart")) {
      likeBtn.classList.remove("bxs-heart");
      likeBtn.classList.add("bx-heart");
      likeBtn.classList.remove("bounce-in");
    } else {
      likeBtn.classList.add("bxs-heart");
      likeBtn.classList.remove("bx-heart");
      likeBtn.classList.add("bounce-in");
    }
  });
});

//! Chart JS

const chartData = {
  labels: ["Workshop", "Theater", "Concert", "Sport"],
  data: [40, 15, 25, 20],
};

const chart = document.getElementById("doughnut");
const eventList = document.querySelector(".chart ul");

new Chart(chart, {
  type: "doughnut",
  data: {
    labels: ["Workshop", "Theater", "Concert", "Sport"],
    datasets: [
      {
        label: "# of Events",
        data: [8, 3, 5, 4],
        backgroundColor: ["#582bac", "#b31a4d", "#e48e2c", "#4a920f"],
        offset: 10,
        hoverOffset: 8,
        hoverBorderColor: "#9a999b",
        borderWidth: 1,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        labels: {
          color: "#8b8a96",
          font: {
            size: 12,
            weight: 600,
          },
        },
      },
    },
    layout: {
      padding: {
        bottom: 10,
      },
    },
  },
});

function population() {
  chartData.labels.forEach((label, i) => {
    let eachEvent = document.createElement("li");
    eachEvent.innerHTML = `${label}: <span class="percentage">${chartData.data[i]}%</span> `;
    eventList.appendChild(eachEvent);
  });
}

population();

function calculate()
{
  var date = document.querySelector('input[name=date').value;
  var a1 = document.querySelector('input[name=builtInEmissions]').value;
  var a2 = document.querySelector('input[name=builtInEmissions]').value;
  var a3 = document.querySelector('input[name=builtInEmissions]').value;
  var a4 = document.querySelector('input[name=builtInEmissions]').value;
  var a5 = document.querySelector('input[name=builtInEmissions]').value;
  var a6 = document.querySelector('input[name=builtInEmissions]').value;
  var a7 = document.querySelector('input[name=builtInEmissions]').value;
  var result = a1 * 0.00149 + a2 * 0.02 + a3 * 0.15 + a4 * 0.4 + a5 * 0.5 + a6 * 1.5 + a7 * 0.8;
  document.querySelector('output[name=co2kg]').value = result;
  var data = {
    'date': date,
    'result': result,
    'csrfmiddlewaretoken': csrftoken
};

var csrftoken = getCookie('csrftoken');

  $.ajax({
    type: "POST",
    url: '/result/',
    data: data, 
    success: function (response) {
        // any process in data
        console.log(response);
    },
    error: function(xhr, status, error) {
      // Handle error response from the server
      console.error(xhr.responseText);
   }
  });
}

// Function to get CSRF cookie value
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Check if the cookie name matches the name parameter
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}