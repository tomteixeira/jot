import { StyleSheet, Text, View } from 'react-native';

export default function IndexScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>jot</Text>
      <Text style={styles.subtitle}>Edit `apps/mobile/app/index.tsx` to get started.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
  },
  title: {
    fontSize: 32,
    fontWeight: '700',
  },
  subtitle: {
    marginTop: 12,
    fontSize: 16,
    opacity: 0.7,
    textAlign: 'center',
  },
});


