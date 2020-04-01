const weeks_epi = document.getElementById("weeks_epi");
const weeks_surg = document.getElementById("weeks_surg");
const time_resumption = document.getElementById("time_resumption");
const baseline_demand = document.getElementById("baseline_demand");
const surg_demand = document.getElementById("surg_demand");
const surg_cap = document.getElementById("surg_cap");
const multi_cap_limitation = document.getElementById("multi_cap_limitation");
const weekly_prop_increase_cap = document.getElementById("weekly_prop_increase_cap");
const num_weeks_run_over = document.getElementById("num_weeks_run_over");
const prop_waiting_dying_covid = document.getElementById("prop_waiting_dying_covid");
const prop_waiting_dying_baseline = document.getElementById("prop_waiting_dying_baseline");

var form = document.getElementById("filterForm");
function handleForm(event) { event.preventDefault(); }
form.addEventListener('submit', handleForm);

const calcButton = document.getElementById("calcButton");
console.log("chart is working");

const chartColors = ['rgba(105, 0, 132, .2)','rgba(247, 68, 55, .2)'];

calcButton.addEventListener('click', () => {
    console.log("calc fired");
    console.log(window.location.href.substring(0, window.location.href.length - 1));
    console.log(window.location.href + "/calculate/" + weeks_epi.value + "/" +
              weeks_surg.value + "/" + time_resumption.value + "/" + baseline_demand.value + "/" + surg_demand.value +
              "/" + surg_cap.value + "/" + multi_cap_limitation.value + "/" + weekly_prop_increase_cap.value + "/" +
              num_weeks_run_over.value + "/" + prop_waiting_dying_covid.value + "/" + prop_waiting_dying_baseline.value);
    var apiCall = new XMLHttpRequest();
          apiCall.onreadystatechange = function() {

            if (this.readyState == 4 && this.status == 200) {

              console.log(this.responseText);
              let outCome = JSON.parse(this.responseText);
              let chart = drawChart();
              updateChart(chart, outCome);
            }
          };
          apiCall.open("GET", window.location.href.substring(0, window.location.href.length - 1) + "/calculate/" + weeks_epi.value + "/" +
              weeks_surg.value + "/" + time_resumption.value + "/" + baseline_demand.value + "/" + surg_demand.value +
              "/" + surg_cap.value + "/" + multi_cap_limitation.value + "/" + weekly_prop_increase_cap.value + "/" +
              num_weeks_run_over.value + "/" + prop_waiting_dying_covid.value + "/" + prop_waiting_dying_baseline.value,
              true);
          apiCall.send();
});

// document.onreadystatechange = () => {
//     if (document.readyState === 'complete') {
//
//         console.log("index_charting.js ready");
// //        loadChartData(defaultDates);
//
//         filterButton.addEventListener("click", function(event){
//             event.preventDefault();
//             console.log("clicked filter button");
//
//             //reload chart data with dates
//             var startDate = filterForm.elements.namedItem("startDate").value;
//             var endDate = filterForm.elements.namedItem("endDate").value;
//
//             dates = {
//                 startDate: startDate,
//                 endDate: endDate
//             };
//
//             params = generateQueryParams(dates);
//
//             loadChartData(params);
//
//         });
//
//     }
//   };

  // function loadChartData(queryParams=""){
  //     var apiCall = new XMLHttpRequest();
  //     apiCall.onreadystatechange = function(){
  //         if(this.readyState == 4 && this.status == 200){
  //             var data = JSON.parse(this.responseText);
  //             console.log(data);
  //
  //             chart = drawChart();
  //
  //             var dataLength = data["index_reading"].length;
  //             for(var i = 0; i < dataLength; i++){
  //                 updateChart(chart, data["index_reading"][i]);
  //             }
  //         }
  //     };
  //
  //     apiCall.open('GET', window.location.protocol + "//" + window.location.host +
  //     "/api/indexreading/" + accountID + "/chart/" + indexID + queryParams, true);
  //     apiCall.send();
  // }

  function updateChart(chart, indexReadingData){
    console.log("update chart");

    //add dates as label for x-axis
    for(var i = 0; i < indexReadingData["WEEK"].length; i++){
        chart.data.labels.push(indexReadingData["WEEK"][i]);
    }

    //add data (currently only adding data for like raio)
    let NewDemand = {
        label: "New Demand",
        data: indexReadingData["NEW_DEMAND"],
        backgroundColor: ['rgba(105, 0, 132, .2)',],
        borderColor: ['rgba(200, 99, 132, .7)',],
        borderWidth: 2
    };

    let Capacity = {
        label: "Capacity",
        data: indexReadingData["CAPACITY"],
        backgroundColor: ['rgba(205, 10, 232, .2)',],
        borderColor: ['rgba(300, 199, 232, .7)',],
        borderWidth: 2
    };

    let RemainingCr = {
        label: "Remaining CR",
        data: indexReadingData["REMAINING_CR"],
        backgroundColor: ['rgba(305, 20, 332, .2)',],
        borderColor: ['rgba(400, 299, 332, .7)',],
        borderWidth: 2
    };

    let MeanWait = {
        label: "Mean Wait",
        data: indexReadingData["MEAN_WAIT"],
        backgroundColor: ['rgba(105, 0, 0, .2)',],
        borderColor: ['rgba(200, 99, 0, .7)',],
        borderWidth: 2,
        hidden: true
    };

    chart.data.datasets.push(NewDemand);
    chart.data.datasets.push(Capacity);
    chart.data.datasets.push(RemainingCr);
    chart.data.datasets.push(MeanWait);
    chart.update();
  }

  function drawChart(){

    var ctxL = document.getElementById("lineChart").getContext('2d');
    console.log("this is firing");
    var myLineChart = new Chart(ctxL, {
      type: 'line',
      options: {
        responsive: true
      }
    });

    return myLineChart;

  }