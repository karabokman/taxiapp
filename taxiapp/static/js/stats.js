

const getChartData = () =>{
    fetch("income-by-category")
    .then((res) => res.json())
    .then((results) =>{
        console.log("results",results);

    });
};

getChartData();