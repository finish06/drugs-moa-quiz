import React, { Component } from 'react';
import axios from '../../axios-orders';

import Aux from '../../hoc/Aux';

import Question from '../../components/Question/Question'
import Answers from '../../components/Answers/Answers'

class Questionaire extends Component {
    constructor(props) {
        super(props);
        this.state = {
            drugs: [],
            moa: [],
            answer: '',
            current_drug: '',
            current_question: 0,
            total_questions: 10,
            correct_answers: 0,
            quizCompleted: false,
            loading: false,
            error: null,
            top_200: [
                'lisinopril',
                'atorvastatin calcium',
                'amlodipine besylate',
                'metoprolol tartrate',
                'simvastatin',
                'losartan potassium',
                'albuterol sulfate',
                'sertraline hydrochloride',
            ]
        };
    }

    getQuestionDrug = () => {
        const drug = this.state.top_200[Math.floor(Math.random() * this.state.top_200.length)];
        console.log(drug)
        this.setState({
            current_drug: drug
        })
        this.getAnswerMoa(drug)
    }

    getMoa = () => {
        const url = '/api/drug/moa/?format=json';
        let db_moa = [];

        this.setState({ loading: true, error: null });

        axios.get(url)
            .then(response => {
                // Validate response data
                if (response?.data && Array.isArray(response.data)) {
                    for (const moaObj of response.data) {
                        if (moaObj?.moa) {
                            db_moa.push(moaObj.moa);
                        }
                    }

                    if (db_moa.length === 0) {
                        throw new Error('No MOA data received from server');
                    }

                    this.setState({
                        moa: [...db_moa],
                        loading: false
                    });
                } else {
                    throw new Error('Invalid response format from server');
                }
            })
            .catch(error => {
                console.error('Error fetching MOAs:', error);
                const errorMessage = error.response?.data?.detail ||
                                   error.message ||
                                   'Failed to load answer options. Please check your connection and try again.';
                this.setState({
                    error: errorMessage,
                    loading: false
                });
            })
    }

    getAnswerMoa = (drug) => {
        const url = '/api/drug/drugs/?format=json&generic=' + encodeURIComponent(drug);

        this.setState({ loading: true, error: null });

        axios.get(url)
            .then(response => {
                // Validate response data with optional chaining
                if (response?.data && Array.isArray(response.data) && response.data.length > 0) {
                    const drugData = response.data[0];
                    const drug_answer = drugData?.moa?.[0]?.moa || '';

                    if (!drug_answer) {
                        throw new Error(`No MOA found for drug: ${drug}`);
                    }

                    this.setState({
                        answer: drug_answer,
                        loading: false
                    });
                } else {
                    throw new Error(`Drug not found: ${drug}`);
                }
            })
            .catch(error => {
                console.error('Error fetching drug answer:', error);
                const errorMessage = error.response?.data?.detail ||
                                   error.message ||
                                   'Failed to load question data. Please try again.';
                this.setState({
                    error: errorMessage,
                    loading: false
                });
                // Try loading another drug
                this.getQuestionDrug();
            })
    }

    getQuestionAnswer = (drug) => {
        const url = '/api/drug/drugs/?format=json&generic=' + encodeURIComponent(drug);
        let db_drugs = [];

        axios.get(url)
            .then(response => {
                // Validate response data with optional chaining
                if (response?.data && Array.isArray(response.data)) {
                    for (const drugData of response.data) {
                        if (drugData?.generic_name) {
                            db_drugs.push({
                                'key': drugData.id || Math.random(),
                                'generic': drugData.generic_name,
                                'brand': drugData
                            });
                        }
                    }
                    this.setState({
                        drugs: [...db_drugs]
                    });
                } else {
                    console.warn('Invalid response format for drug details');
                }
            })
            .catch(error => {
                console.error('Error fetching drug details:', error);
                // Non-critical error, don't show to user
            })
    }

    checkAnswerClickHandler = (moa) => {
        const isCorrect = moa === this.state.answer;
        const nextQuestion = this.state.current_question + 1;
        const isLastQuestion = nextQuestion >= this.state.total_questions;

        if (isCorrect) {
            this.setState({
                correct_answers: this.state.correct_answers + 1,
                current_question: nextQuestion,
                quizCompleted: isLastQuestion
            })
        }
        else {
            this.setState({
                current_question: nextQuestion,
                quizCompleted: isLastQuestion
            })
        }

        // Only get next question if quiz is not complete
        if (!isLastQuestion) {
            this.getQuestionDrug()
        }
    }

    restartQuiz = () => {
        this.setState({
            current_question: 0,
            correct_answers: 0,
            quizCompleted: false,
            answer: '',
            current_drug: ''
        });
        this.getQuestionDrug();
    }

    handleRetry = () => {
        // Clear error and reload data
        this.setState({
            error: null,
            loading: true
        });
        this.getQuestionDrug();
        this.getMoa();
    }

    componentDidMount() {
        this.getQuestionDrug()
        this.getMoa()
    }

    render() {
        const { loading, error, current_drug, answer, moa, quizCompleted, correct_answers, total_questions } = this.state;

        // Calculate percentage
        const percentage = Math.round((correct_answers / total_questions) * 100);

        return (
            <Aux>
                {error && (
                    <div style={{
                        padding: '20px',
                        margin: '20px',
                        backgroundColor: '#f8d7da',
                        color: '#721c24',
                        border: '1px solid #f5c6cb',
                        borderRadius: '4px',
                        textAlign: 'center'
                    }}>
                        <strong>Error:</strong> {error}
                        <br />
                        <button
                            onClick={this.handleRetry}
                            style={{
                                marginTop: '15px',
                                padding: '10px 20px',
                                backgroundColor: '#721c24',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                cursor: 'pointer',
                                fontSize: '14px',
                                fontWeight: 'bold'
                            }}
                            onMouseOver={(e) => e.target.style.backgroundColor = '#5a1419'}
                            onMouseOut={(e) => e.target.style.backgroundColor = '#721c24'}
                        >
                            Retry
                        </button>
                    </div>
                )}
                {loading && (
                    <div style={{
                        padding: '20px',
                        margin: '20px',
                        textAlign: 'center',
                        fontSize: '18px',
                        color: '#007bff'
                    }}>
                        Loading...
                    </div>
                )}
                {!loading && !error && quizCompleted && (
                    <div style={{
                        padding: '40px',
                        margin: '20px auto',
                        maxWidth: '600px',
                        textAlign: 'center',
                        backgroundColor: '#d4edda',
                        border: '1px solid #c3e6cb',
                        borderRadius: '8px'
                    }}>
                        <h2 style={{ color: '#155724', marginBottom: '20px' }}>Quiz Complete!</h2>
                        <div style={{ fontSize: '24px', marginBottom: '10px' }}>
                            <strong>Your Score:</strong>
                        </div>
                        <div style={{ fontSize: '48px', fontWeight: 'bold', color: '#155724', marginBottom: '10px' }}>
                            {correct_answers} / {total_questions}
                        </div>
                        <div style={{ fontSize: '32px', color: '#155724', marginBottom: '30px' }}>
                            {percentage}%
                        </div>
                        <button
                            onClick={this.restartQuiz}
                            style={{
                                padding: '15px 40px',
                                fontSize: '18px',
                                backgroundColor: '#28a745',
                                color: 'white',
                                border: 'none',
                                borderRadius: '5px',
                                cursor: 'pointer',
                                fontWeight: 'bold'
                            }}
                            onMouseOver={(e) => e.target.style.backgroundColor = '#218838'}
                            onMouseOut={(e) => e.target.style.backgroundColor = '#28a745'}
                        >
                            Restart Quiz
                        </button>
                    </div>
                )}
                {!loading && !error && !quizCompleted && (
                    <>
                        <Question
                            drug={current_drug}
                            currentQuestion={this.state.current_question}
                            totalQuestions={this.state.total_questions}>
                        </Question>
                        <Answers
                            position={Math.floor(Math.random() * 4) + 1}
                            correct={answer}
                            options={moa}
                            checkAnswer={this.checkAnswerClickHandler}>
                        </Answers>
                    </>
                )}
            </Aux>
        );
    }
}

export default Questionaire;