import React from 'react';

import Aux from '../../hoc/Aux'


const question = (props) => {
    return (
        <Aux>
            {props.currentQuestion !== undefined && props.totalQuestions !== undefined && (
                <div
                    style={{
                        textAlign: 'center',
                        fontSize: '18px',
                        color: '#666',
                        marginBottom: '10px',
                        fontWeight: '500'
                    }}
                    role="status"
                    aria-live="polite"
                    aria-label={`Progress: Question ${props.currentQuestion + 1} of ${props.totalQuestions}`}
                >
                    Question {props.currentQuestion + 1} of {props.totalQuestions}
                </div>
            )}
            <h2 role="heading" aria-level="2" id="quiz-question">
                What is the mechanism of action of <span aria-label={`drug: ${props.drug}`}>{props.drug}</span>?
            </h2>
        </Aux>
    )
}

export default question
