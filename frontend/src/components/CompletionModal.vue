<template>
  <div class="modal fade" id="completionModal" tabindex="-1" aria-labelledby="completionModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="completionModalLabel">Complete Appointment</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitForm">
            <div class="mb-3">
              <label for="diagnosis" class="form-label">Diagnosis</label>
              <textarea class="form-control" id="diagnosis" v-model="form.diagnosis" rows="3"></textarea>
            </div>
            <div class="mb-3">
              <label for="prescription" class="form-label">Prescription</label>
              <textarea class="form-control" id="prescription" v-model="form.prescription" rows="3"></textarea>
            </div>
            <div class="mb-3">
              <label for="notes" class="form-label">Notes</label>
              <textarea class="form-control" id="notes" v-model="form.notes" rows="2"></textarea>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
              <button type="submit" class="btn btn-primary">Save</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CompletionModal",
  data() {
    return {
      form: {
        diagnosis: "",
        prescription: "",
        notes: ""
      }
    };
  },
  methods: {
    submitForm() {
      this.$emit("submit", this.form);
    }
  }
};
</script>