<template>
    <h1 class="title text-center">Willkommen im Prüfungssimulator 🎣</h1>
    <div v-if="!this.loading && !this.errored">
        <div v-for="(category, categoryindex) in quizdata" v-bind:key="category" class="category">
            <h2 class="fw-bold">{{category.name}}</h2>
            <h3 v-if="shouldevaluate">{{category.solvedCorrectly}} / 12</h3>
                <QuizElement v-for="(question, questionindex) in category.questions" 
                v-bind:key="question"
                v-bind:question="question.question"
                v-bind:answers="question.answers"
                v-bind:solution="question.solution"
                v-bind:image="question.image"
                v-bind:shouldevaluate="shouldevaluate"
                v-bind:id="categoryindex + '_' + questionindex"
                v-on:evaluated="questionEvaluated"/>
            <br/>
        </div>

        <button v-on:click="startEvaluation()" v-if="!shouldevaluate" class="btn btn-primary">Auswerten!</button>

        <div v-if="shouldevaluate">
            <h2 class="fw-bold" v-if="passedExam">Bestanden 🎉</h2><h2 class="fw-bold" v-else>Nicht bestanden 😪</h2>
            <table class="table table-striped">
            <thead>
                <tr>
                    <th>Kategorie</th>
                    <th>Erreichte Punkte</th>
                    <th>Maximale Punktzahl</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="category in quizdata" v-bind:key="category" v-bind:class="{'table-danger': category.solvedCorrectly < 6}">
                    <td>{{category.name}}</td>
                    <td>{{category.solvedCorrectly}}</td>
                    <td>12</td>
                </tr>
                <tr v-bind:class="{'table-danger': sumSolvedCorrectly < 45}">
                    <td>&sum;</td>
                    <td>{{sumSolvedCorrectly}}</td>
                    <td>60</td>
                </tr>
                </tbody>
            </table>    
        </div>

        <h6 class="text-center text-secondary" v-on:click="share" v-if="this.sharable">Klick hier um das Quiz zu teilen!</h6>
        <h6 class="text-center" v-else>Du willst dieses Quiz teilen? Dann benutze diese URL: {{quizurl}} </h6>
    </div>
    <div v-if="this.errored">Fehler beim Laden der QuizApp. Bitte kontaktiere den Entwickler!</div>
</template>

<script>
import axios from 'axios';
import QuizElement from './QuizElement.vue';

export default {
  name: "Quiz",
  data() {
    return {
        quizdata: null,
        errored: false,
        loading: true,
        shouldevaluate: false,
        quizurl: null,
        sumSolvedCorrectly: 0,
        seed: Date.now(),
        sharable: typeof navigator.share !== "undefined",
    };
  },
  methods: {
      startEvaluation: function(){
          this.shouldevaluate = true
      },
      questionEvaluated: function(id, correct){
          let category = id.split('_')[0]
          this.quizdata[category]['solvedCorrectly'] = (this.quizdata[category]['solvedCorrectly']|| 0) + (correct ? 1 : 0);
          this.sumSolvedCorrectly = (this.sumSolvedCorrectly) + (correct ? 1 : 0);
      },
      share: function(){
           if (navigator.share) {
                navigator.share({
                    title: 'Fischereiprüfung Simulator',
                    url: this.quizurl
                }).then(() => {
                    console.log('Thanks for sharing!');
                })
                .catch(console.error);
            }
      }
  },
  mounted() {
    let urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('quizid')){
        this.seed = urlParams.get('quizid')
    }

    this.quizurl = location.protocol + '//' + location.host + location.pathname + '?quizid=' + this.seed

    axios
      .get("quiz/" + this.seed)
      .then((response) => {
        this.quizdata = response.data;
      })
      .catch((error) => {
        console.log(error);
        this.errored = true;
      })
      .finally(() => (this.loading = false));
  },
  computed: {
      passedExam: function(){
          for (let category in this.quizdata){
              if (this.quizdata[category]['solvedCorrectly'] < 6){
                  return false
              }
          }
          return this.sumSolvedCorrectly >= 45
      }
  },
  components: {
      QuizElement
  }
};
</script>

<style>
.category:not(:last-of-type){
    margin-bottom: 2em;
}

.title {
     margin-bottom: 2em;
 }
</style>