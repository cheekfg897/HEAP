<template>
  <div>
    <h1>Generate QR Ticket and Send Email</h1>
    <form @submit.prevent="sendEmail">
      <div>
        <label for="attendeeName">Attendee Name:</label>
        <input v-model="attendeeName" type="text" id="attendeeName" required />
      </div>
      <div>
        <label for="attendeeEmail">Attendee Email:</label>
        <input v-model="attendeeEmail" type="email" id="attendeeEmail" required />
      </div>
      <div>
        <label for="eventName">Event Name:</label>
        <input v-model="eventName" type="text" id="eventName" required />
      </div>
      <div>
        <label for="eventDate">Event Date:</label>
        <input v-model="eventDate" type="date" id="eventDate" required />
      </div>
      <div>
        <label for="eventLocation">Event Location:</label>
        <input v-model="eventLocation" type="text" id="eventLocation" required />
      </div>
      <button type="submit">Send QR Ticket</button>
    </form>

    <div v-if="message" :class="messageType">
      {{ message }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      attendeeName: "",
      attendeeEmail: "",
      eventName: "",
      eventDate: "",
      eventLocation: "",
      message: "",
      messageType: ""
    };
  },
  methods: {
    async sendEmail() {
      const payload = {
        attendeeName: this.attendeeName,
        attendeeEmail: this.attendeeEmail,
        eventName: this.eventName,
        eventDate: this.eventDate,
        eventLocation: this.eventLocation
      };

      try {
        const response = await fetch("http://localhost:5000/send_email_python", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (response.ok) {
          this.message = result.message;
          this.messageType = "success";
        } else {
          this.message = result.message;
          this.messageType = "error";
        }
      } catch (error) {
        this.message = "An error occurred while sending the email.";
        this.messageType = "error";
      }
    }
  }
};
</script>

<style scoped>
.success {
  color: green;
}
</style>