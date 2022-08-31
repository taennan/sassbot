<script lang="ts">
  import Button, { Label } from "@smui/button";
  import Center from "./Center.svelte";
  import Space from "./Space.svelte";

  import { createEventDispatcher } from "svelte";

  const dispatchPerformance = createEventDispatcher();

  function sendPerf(correct: boolean) {
    const res = correct ? "correct" : "wrong";
    console.log(`Result was ${res}`);
    dispatchPerformance("performanceSent", res);
  }
</script>

<main>
  <Center>
    <p>Was that response correct?</p>
  </Center>

  <Center>
    <Button
      color="primary"
      variant="outlined"
      on:click={() => {
        sendPerf(true);
      }}
    >
      <Label>Yes</Label>
    </Button>
    <Button
      color="primary"
      variant="outlined"
      on:click={() => {
        sendPerf(false);
      }}
    >
      <Label>No</Label>
    </Button>
  </Center>
</main>
