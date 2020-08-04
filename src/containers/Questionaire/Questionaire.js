import React, { Component } from 'react';
import axios from '../../axios-orders';

import '../../config';

import Aux from '../../hoc/Aux';

import Banner from '../../components/Banner/Banner';
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
        axios.get(url)
            .then(response => {
                for (const moa in response.data) {
                    db_moa.push(response.data[moa]['moa'])
                }
                this.setState({
                    moa: [...db_moa]
                });
            })
            .catch(error => {
                console.log(error);
            })
    }

    getAnswerMoa = (drug) => {
        const url = '/api/drug/drugs/?format=json&generic=' + drug;
        axios.get(url)
            .then(response => {
                let drug_answer = '';
                for (const drug in response.data) {
                    drug_answer = response.data[drug]['moa'][0]['moa']
                    if (drug_answer) {
                        break;
                    }
                }
                this.setState({
                    answer: drug_answer
                })
            })
            .catch(error => {
                console.log(error)
            })
        console.log(this.state.answer)
    }

    getQuestionAnswer = (drug) => {
        const url = '/api/drug/drugs/?format=json&generic=' + drug;
        let db_drugs = [];
        axios.get(url)
            .then(response => {
                for (const key in response.data) {
                    db_drugs.push({'key': key, 'generic': response.data[key]['generic_name'], 'brand': response.data[key]})
                };
                this.setState({
                    drugs: [...db_drugs]
                })
            })
            .catch(error => {
                console.log(error)
            })
    }

    checkAnswerClickHandler = (moa) => {
        if (moa === this.state.answer) {
            this.setState({
                correct_answers: this.state.correct_answers + 1,
                current_question: this.state.current_question + 1
            })    
        }
        else {
            this.setState({
                current_question: this.state.current_question + 1
            })
        }
        console.log(this.state.correct_answers)
        this.getQuestionDrug()
    }

    componentDidMount() {
        this.getQuestionDrug()
        this.getMoa()
    }

    render() {
        return (
            <Aux>
                <Question drug={this.state.current_drug}></Question>
                <Answers
                    position={Math.floor(Math.random() * 4) + 1}
                    correct={this.state.answer}
                    options={this.state.moa}
                    checkAnswer={this.checkAnswerClickHandler}>
                </Answers>
            </Aux>
        );
    }
}

export default Questionaire;