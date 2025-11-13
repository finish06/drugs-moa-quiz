import React from 'react';

import Aux from '../../hoc/Aux'


const answers = (props) => {
    let listAnswers = [];
    // Filter out the correct answer from available options to avoid duplicates
    const availableOptions = props.options.filter(option => option !== props.correct);
    const selectedIncorrect = new Set();

    for (let i = 1; i <= 4; i++){
        if (props.position === i) {
            console.log('Correct: ' +  props.correct)
            listAnswers.push(props.correct);
        }
        else {
            // Select a unique incorrect answer
            let altOption;
            do {
                altOption = availableOptions[Math.floor(Math.random() * availableOptions.length)];
            } while (selectedIncorrect.has(altOption));

            selectedIncorrect.add(altOption);
            console.log(altOption);
            listAnswers.push(altOption);
        }
    }
    return (
        <Aux>
            <ul>
                {listAnswers.map((answer, index) =>
                    <li key={index} onClick={() => props.checkAnswer(answer)}>{answer}</li>
                )}
            </ul>
        </Aux>
    )
}

export default answers