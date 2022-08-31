<script lang="ts">
  import SpeechBalloon from "./SpeechBalloon.svelte";
  import Center from "./Center.svelte";

  import { fly } from "svelte/transition";

  export let humanText: string;
  export let robotText: string;

  export let fadeTime: number = 600;
  export let fadeDist: number = 75;
</script>

<main>
  <section transition:fly={{ x: -fadeDist, duration: fadeTime }}>
    <Center>
      <SpeechBalloon text={humanText ? humanText : "..."} face="left" />
    </Center>
    <Center>
      <img src="Man.jpg" alt="Man" />
    </Center>
  </section>

  <section
    in:fly={{
      x: fadeDist,
      delay: fadeTime + 100,
      duration: fadeTime,
    }}
    out:fly={{ x: fadeDist, duration: fadeTime }}
  >
    <Center>
      <SpeechBalloon
        text={!robotText ? "Bleep bloop" : robotText}
        face="right"
      />
    </Center>
    <Center>
      <img src="Bot.jpg" alt="Bot" />
    </Center>
  </section>
</main>

<style lang="scss">
  main {
    display: flex;
    justify-content: center;

    section {
      width: 40%;
      height: 0%;

      img {
        margin-left: auto;
        margin-right: auto;

        // Height is set to 0% an images to keep scale
        // - Doesn't work if width is 0%
        &[alt="Man"] {
          width: 40%;
          height: 0%;
        }
        &[alt="Bot"] {
          // Properties 'margin-top' and 'width' should add up to the
          // Man image width x 2 to keep bottom of both images alined
          margin-top: 5%;
          width: 75%;
          height: 0%;
        }
      }
    }
  }
</style>
