<template>
    <div class="question">
        <h4>
            <span v-if="evaluated">
                <span v-if="solvedcorrectly">✔</span>
                <span v-else>❌</span>
            </span>
            {{question}}
        </h4>
        <img :src="require(`@/assets/${image}`)" v-if="image" class="img-fluid"/>
        <h6 v-if="solution.length > 1">(2 Antworten sind gefragt!)</h6>
        <form class="form-check" :id="id">
            <div v-for="(answer, index) in answers" :key="answer">
                <div>
                    <input class="form-check-input" type="checkbox" :disabled="evaluated" :id="id+index" :value="index" v-model="selectedanswers">
                    <label class="form-check-label" :for="id+index">{{answer}}</label>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
export default {
    name: 'QuizElement',
    emits: ['evaluated'],
    data(){
        return {
            selectedanswers: [],
            solvedcorrectly: false,
            evaluated: false
        }
    },
    props: {
        question: null,
        answers: null,
        solution: null,
        image: null,
        id: null,
        shouldevaluate: null,
    },
    watch: {
        shouldevaluate: function() {
            this.evaluate()
        }
    },
    methods:{
        evaluate(){
            this.solvedcorrectly = true

            for (let i = 0; i < 3; i++){
                let checkboxElement= document.getElementById(this.id + i)
                let checkboxIsChecked = checkboxElement.checked
                checkboxElement.parentNode.style.color = this.solution.includes(i) ? 'green' : 'red'
                let checkbox_right_clicked = (checkboxIsChecked && this.solution.includes(i)) || (!checkboxIsChecked && !this.solution.includes(i))
                if (!checkbox_right_clicked)
                    this.solvedcorrectly = false

            }
            this.$emit('evaluated', this.id, this.solvedcorrectly)
            this.evaluated = true
        }
    }
}
</script>

<style>
.question{
    margin-bottom: 2em;
}
</style>