const serverURL = `${location.protocol}//${location.host}`;
const apiURL = `${serverURL}/api/v1`;

function requestTasksInfo() {
    fetch(`${apiURL}/tasks`)
        .then((res) => res.json())
        .then((res) => {
            const prettyJSON = JSON.stringify(res, null, 2);
            const acknowledgeResultField = document.getElementById('acknowledgeResultField');
            acknowledgeResultField.innerHTML = prettyJSON;
        })
        .catch((err) => {
            console.log(err);
        });
}

function postNewMakeDecisionTask() {
    const makeDecisionResultField = document.getElementById('makeDecisionResultField');
    makeDecisionResultField.innerHTML = '';

    const createNewTaskRequestPayloadField = document.getElementById('makeDecisionRequestPayloadField');
    let payload;
    if (createNewTaskRequestPayloadField.value === '') {
        payload = JSON.parse(data);
    } else {
        payload = JSON.parse(createNewTaskRequestPayloadField.value);
    }

    const config = {
        method: 'POST',
        body: JSON.stringify(payload),
        headers: {
            "content-type": "application/json"
        }
    };
    fetch(`${apiURL}/make-decision`, config)
        .then((res) => res.json())
        .then((res) => {
            const prettyJSON = JSON.stringify(res, null, 2);
            const makeDecisionResultField = document.getElementById('makeDecisionResultField');
            makeDecisionResultField.innerHTML = prettyJSON;
        })
        .catch((err) => {
            const makeDecisionResultField = document.getElementById('makeDecisionResultField');
            makeDecisionResultField.innerHTML = 'Error! ' + err;
        });
}

function init() {
    const acknowledgeButton = document.getElementById('acknowledgeButton');
    const makeDecisionButton = document.getElementById('makeDecisionButton');

    acknowledgeButton.addEventListener('click', function (event) {
        event.preventDefault();
        requestTasksInfo();
    });

    makeDecisionButton.addEventListener('click', function (event) {
        event.preventDefault();
        postNewMakeDecisionTask();
    });
}
