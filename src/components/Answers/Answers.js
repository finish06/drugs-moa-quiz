import React from 'react';

import Aux from '../../hoc/Aux'
import classes from './Answers.module.css'


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
            <ul className={classes.answerList}>
                {listAnswers.map((answer, index) =>
                    <li key={index}>
                        <button
                            type="button"
                            className={classes.answerButton}
                            onClick={() => props.checkAnswer(answer)}
                            aria-label={`Answer option ${index + 1}: ${answer}`}
                        >
                            {answer}
                        </button>
                    </li>
                )}
            </ul>
        </Aux>
    )
}

export default answers