<template>
<div v-if="classView">
  <div class="container mt-3" >
      <h3>Lista Classi</h3><br>
      <div v-for="(classroom, index) in classrooms" :key="index">
         <!-- <p><router-link :to="{name: 'subjects', params: {subjects: subjects, id: classroom.id} }" v-on:click="getClassroomSubjects(classroom)" >{{ classroom.class_name }}</router-link></p>
         -->
           <div class="alert alert-info alert-dismissible fade show" role="alert">
              <a href="#" class="alert-link" v-on:click="getClassroomSubjects(classroom)">
                {{ classroom.class_name }}
              </a>
              <button type="button" class="btn-close" aria-label="Close" v-on:click="deleteClassroom(classroom)"></button>
            </div>
      </div>
      <div class="container">
        <br>
        <form @submit.prevent="addClassroom">
          <input type="text" class="form-control mt-3" placeholder="Scrivi la nuova classe" v-model="newClassroom" required><br>
          <button type="submit" class="btn btn-primary">Aggiungi Classe</button>
        </form>
        
      </div>
      
  </div>
      
</div>
<div v-if="subjectView">
  <div class="container mt-3">
        <button type="button" class="btn btn-success" v-on:click="backToClassroom()">Torna alla lista delle Classi</button>
    </div>
    <div class="container mt-3">
      <br>
            <h3>Materie della classe {{ className }}</h3><br>
        <div v-for="(subject, index) in subjects" :key="index">
            <div class="alert alert-info alert-dismissible fade show" role="alert">
              <a href="#" class="alert-link" v-on:click="getSubjectExercise(subject)">
                {{ subject.name }}
              </a>
              <button type="button" class="btn-close" aria-label="Close" v-on:click="deleteSubject(subject)"></button>
            </div>
        </div>
        <br>
        <form @submit.prevent="addSubject">
          <input type="text" class="form-control mt-3" placeholder="Scrivi la nuova materia" v-model="newSubject" required><br>
          <button type="submit" class="btn btn-primary">Aggiungi Materia</button>
        </form>
    </div>
</div>
  <div v-if="exerciseView">
    
    <div class="container mt-3">
        <button type="button" class="btn btn-success" v-on:click="backToSubject()">Torna alla lista delle Materie</button>
    </div>
    <div class="container mt-3"> 
      <br> 
      <h3>Esercizi di {{ currentSubject.name }} della classe {{ className }}</h3>
      <br>
      <div v-for="(exercise, index) in exercises" :key="index">
          <div class="alert alert-info alert-dismissible fade show" role="alert">
              {{ exercise.title }}

              <button type="button" class="btn-close" aria-label="Close" v-on:click="deleteExercise(exercise)"></button>
            </div>
      </div>
      <br>
        <form @submit.prevent="addExercise">
          <input type="text" class="form-control mt-3" placeholder="Scrivi il nuovo esercizio" v-model="newExercise" required><br>
          <button type="submit" class="btn btn-primary">Aggiungi Esercizio</button>
        </form>
    </div>
  </div>
  


  
</template>

<script>
import axios from 'axios';
export default {
  name: 'EserciziClassi',
  data() {
    return {
      classrooms: [],
      subjects: [],
      exercises: [],
      classView: true,
      subjectView: false,
      exerciseView: false,
      className: '',
      currentClassroom: {},
      currentSubject: {},
      newClassroom: '',
      newSubject: '',
      newExercise: ''
    };
  },
  methods: {
    getClassrooms() {
      axios.get('/classrooms/')
        .then((res) => {
          this.classrooms = res.data;
          console.log(this.classrooms)
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getClassroomSubjects(classroom) {
      axios.get('/classrooms/' + String(classroom.id) + '/subjects/')
        .then((res) => {
          this.className = classroom.class_name
          this.currentClassroom = classroom;
          this.subjects = res.data;
          console.log(this.subjects)
          console.log(this.classView)
          console.log(this.subjectView)
          this.classView=false
          this.subjectView=true
          console.log(this.classView)
          console.log(this.subjectView)
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getSubjectExercise(subject){
      this.exerciseView = true
      this.subjectView=false
      this.currentSubject = subject
      axios.get('/classrooms/'+String(this.currentClassroom.id)+'/'+String(this.currentSubject.id)+'/exercises/')
        .then((res) => {
          this.exercises = res.data;
          console.log(this.exercises)
        })
        .catch((error) => {
          console.error(error);
        });
    },
    backToSubject(){
      this.exerciseView = false
      this.subjectView=true
    },
    backToClassroom(){
      this.classView=true
      this.subjectView=false
    },
    deleteClassroom(classroom){
        axios.delete('/classrooms/'+ String(classroom.id) +'/')
        .then((res) => {
          console.log(res.data)
          this.getClassrooms();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addClassroom(){
      console.log(this.newClassroom)
      let obj= {}
      obj['class_name'] = this.newClassroom
      axios.post('/classrooms/', obj)
        .then((res) => {
          console.log(res.data)
          this.getClassrooms();
        })
        .catch((error) => {
          console.error(error);
        });
      this.newClassroom = ''
      
    },
    deleteSubject(subject){
        axios.delete('/classrooms/'+ String(this.currentClassroom.id) +'/' + String(subject.id) +'/')
        .then((res) => {
          console.log(res.data)
          this.getClassroomSubjects(this.currentClassroom);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addSubject(){
      console.log(this.newSubject)
      let obj= {}
      obj['name'] = this.newSubject
      axios.post('/classrooms/'+ String(this.currentClassroom.id) +'/subjects/', obj)
        .then((res) => {
          console.log(res.data)
          this.getClassroomSubjects(this.currentClassroom);
        })
        .catch((error) => {
          console.error(error);
        });
      this.newSubject = ''
    },
    deleteExercise(exercise){
      axios.delete('/classrooms/'+ String(this.currentClassroom.id) +'/' + String(this.currentSubject.id) +'/'+String(exercise.id)+'/')
        .then((res) => {
          console.log(res.data)
          this.getSubjectExercise(this.currentSubject);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addExercise(){
      console.log(this.newExercise)
      let obj= {}
      obj['title'] = this.newExercise
      axios.post('/classrooms/'+ String(this.currentClassroom.id) +'/' + String(this.currentSubject.id) +'/exercises/', obj)
        .then((res) => {
          console.log(res.data)
          this.getSubjectExercise(this.currentSubject);
        })
        .catch((error) => {
          console.error(error);
        });
      this.newExercise = ''
    }
  },
  created() {
    this.getClassrooms();
  },
};
</script>



