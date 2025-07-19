export const getWaveformColor = (title: string): string | undefined => {
  title = title.toLowerCase();
  switch (title) {
    case "bass":
      return "#dfc768";
    case "drums":
      return "#64d878";
    // case "guitar":
    //   return "#7289f3";
    case "vocals":
      return "#f37e7e";
    // case "keys":
    //   return "#e87777";
    case "other":
      return "#7289f3";
    default:
      return undefined;
  }
};
