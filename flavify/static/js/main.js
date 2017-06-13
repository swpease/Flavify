function numIngsSorter(a, b) {
    if (a.numings < b.numings) return -1;
    if (a.numings > b.numings) return 1;
    return 0;
}
