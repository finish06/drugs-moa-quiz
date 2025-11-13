import React from 'react';

import Aux from '../../hoc/Aux'


const question = (props) => {
    return (
        <Aux>
            {props.currentQuestion !== undefined && props.totalQuestions !== undefined && (
                <div style={{
                    textAlign: 'center',
                    fontSize: '18px',
                    color: '#666',
                    marginBottom: '10px',
                    fontWeight: '500'
                }}>
                    Question {props.currentQuestion + 1} of {props.totalQuestions}
                </div>
            )}
            <h2>What is the mechanism of action of {props.drug}?</h2>
        </Aux>
    )
}

export default question