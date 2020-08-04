import React from 'react';

import Aux from '../../hoc/Aux'


const answers = (props) => {
    let listAnswers = [];
    for (let i = 1; i <= 4; i++){
        if (props.position === i) {
            console.log('Correct: ' +  props.correct)
            listAnswers.push(props.correct);
        }
        else {
            const altOption = props.options[Math.floor(Math.random() * props.options.length)]
            console.log(altOption);
            listAnswers.push(altOption)
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