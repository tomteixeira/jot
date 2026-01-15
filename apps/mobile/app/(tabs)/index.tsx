import { StyleSheet, View } from 'react-native';

import { HomeInputDock } from '@/src/features/home/components/HomeInputDock';
import { COLORS } from '@/src/theme/colors';
import { LAYOUT } from '@/src/theme/layout';

export default function HomeScreen() {
  return (
    <View style={styles.screen}>
      <HomeInputDock />
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: LAYOUT.flexFull,
    backgroundColor: COLORS.backgroundPrimary,
  },
});


